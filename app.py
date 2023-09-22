from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataBaseModel import TCNK_Table, TMH_Table, YHTHVB_Table, DDVTP_Table, YHN_Table
from extractInformation import extract_information_ddvtp, extract_information_tcnk, extract_information_tmh, \
    extract_information_yhn, extract_information_yhthvb
from extractInformation import export_table_to_csv, create_zip_file
from flask import send_file
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

db_engine = create_engine('sqlite:///information.db')
Session = sessionmaker(bind=db_engine)

tcnk_zip_url = None
yhthvb_zip_url = None
ddvtp_zip_url = None
yhn_zip_url = None
tmh_zip_url = None
crawling_status = ""
download_urls = []


@app.route('/')
def home():
    return render_template('home.html', tcnk_zip_url=tcnk_zip_url, tmh_zip_url=tmh_zip_url,
                           yhthvb_zip_url=yhthvb_zip_url, ddvtp_zip_url=ddvtp_zip_url, yhn_zip_url=yhn_zip_url)


@socketio.on('process_urls')
def process_urls(choices):
    thread = threading.Thread(target=perform_extraction, args=(choices,))
    thread.start()


def perform_extraction(choices):
    global crawling_status, download_urls,tcnk_zip_url, tmh_zip_url, yhthvb_zip_url, ddvtp_zip_url, yhn_zip_url
    tcnk_zip_url = tmh_zip_url = yhthvb_zip_url = ddvtp_zip_url = yhn_zip_url
    crawling_status = "in_progress"
    socketio.emit('status_update', {"status": "in-progress"}, namespace='/')
    print(choices)
    response_data = {
        "tcnkZipUrl": None,
        "tmhZipUrl": None,
        "yhthvbZipUrl": None,
        "ddvtpZipUrl": None,
        "yhnZipUrl": None
    }
    for choice in choices:
        if choice == 'tcnk':
            extract_information_tcnk('https://tcnhikhoa.vn/index.php/tcnk/issue/archive')
            export_table_to_csv(TCNK_Table, 'tcnk.csv')
            create_zip_file('tcnk.csv', 'tcnk.zip')
            if create_zip_file('tcnk.csv', 'tcnk.zip'):
                tcnk_zip_url = 'tcnk.zip'
                response_data["tcnkZipUrl"] = tcnk_zip_url
                socketio.emit('processing_complete', response_data, namespace='/')
        elif choice == 'tmh':
            extract_information_tmh('https://tapchitaimuihong.vn/index.php/tmh/issue/archive')
            export_table_to_csv(TMH_Table, 'tmh.csv')
            create_zip_file('tmh.csv', 'tmh.zip')
            if create_zip_file('tmh.csv', 'tmh.zip'):
                tmh_zip_url = 'tmh.zip'
                response_data["tmhZipUrl"] = tmh_zip_url
                socketio.emit('processing_complete', response_data, namespace='/')
        elif choice == 'yhthvb':
            extract_information_yhthvb('https://jbdmp.vn/index.php/yhthvb/issue/archive')
            export_table_to_csv(YHTHVB_Table, 'yhthvb.csv')
            create_zip_file('yhthvb.csv', 'yhthvb.zip')
            if create_zip_file('yhthvb.csv', 'yhthvb.zip'):
                yhthvb_zip_url = 'yhthvb.zip'
                response_data["yhthvbZipUrl"] = yhthvb_zip_url
                socketio.emit('processing_complete', response_data, namespace='/')
        elif choice == 'ddvtp':
            extract_information_ddvtp('https://tapchidinhduongthucpham.org.vn/index.php/jfns/issue/archive')
            export_table_to_csv(DDVTP_Table, 'ddvtp.csv')
            create_zip_file('ddvtp.csv', 'ddvtp.zip')
            if create_zip_file('ddvtp.csv', 'ddvtp.zip'):
                ddvtp_zip_url = 'ddvtp.zip'
                response_data["ddvtpZipUrl"] = ddvtp_zip_url
                socketio.emit('processing_complete', response_data, namespace='/')
        elif choice == 'yhn':
            extract_information_yhn('https://tapchinghiencuuyhoc.vn/index.php/tcncyh/issue/archive')
            export_table_to_csv(YHN_Table, 'yhn.csv')
            create_zip_file('yhn.csv', 'yhn.zip')
            if create_zip_file('yhn.csv', 'yhn.zip'):
                yhn_zip_url = 'yhn.zip'
                response_data["yhnZipUrl"] = yhn_zip_url
                socketio.emit('processing_complete', response_data, namespace='/')
    print(response_data)
    crawling_status = "completed"
    download_urls = response_data
    print(download_urls)
    socketio.emit('status_update', {"status": "completed"}, namespace='/')
    socketio.emit('processing_complete', response_data, namespace='/')


@socketio.on('check_status')
def check_status():
    if crawling_status == "completed":
        data = {"status": "completed", "urls": download_urls}
    else:
        data = {"status": crawling_status}
    socketio.emit('status_update', data, namespace='/')


@app.route('/<filename>')
def serve_zip(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    socketio.run(app, debug=True)