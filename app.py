from flask import Flask, render_template, request
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from dataBaseModel import Base, TCNK_Table, TMH_Table, YHTHVB_Table, DDVTP_Table, YHN_Table
from extractInformation import extract_information_ddvtp, extract_information_tcnk, extract_information_tmh, extract_information_yhn, extract_information_yhthvb
from extractInformation import export_table_to_csv, create_zip_file
import csv
import zipfile
import os
app = Flask(__name__)

# Configure the database connection
db_engine = create_engine('sqlite:///information.db')
Session = sessionmaker(bind=db_engine)


@app.route('/', methods=['POST', 'GET'])
def Scrawl():
    tcnk_zip_url = None
    yhthvb_zip_url = None
    ddvtp_zip_url = None
    yhn_zip_url = None
    tmh_zip_url = None

    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        if search:
            urls = search.split(',')
            for url in urls:
                url = url.replace(' ', '')
                if url == 'https://tcnhikhoa.vn/index.php/tcnk/issue/archive':
                    extract_information_tcnk(url)
                    export_table_to_csv(TCNK_Table, 'tcnk.csv')
                    create_zip_file('tcnk.csv', 'tcnk.zip')
                    if create_zip_file('tcnk.csv', 'tcnk.zip'):
                        tcnk_zip_url = 'tcnk.zip'
                elif url == 'https://jbdmp.vn/index.php/yhthvb/issue/archive':
                    extract_information_yhthvb(url)
                    export_table_to_csv('YHTHVB_Table', 'yhthvb.csv')
                    create_zip_file('yhthvb.csv', 'yhthvb.zip')
                    if create_zip_file('yhthvb.csv', 'yhthvb.zip'):
                        yhthvb_zip_url = 'yhthvb.zip'
                elif url == 'https://tapchidinhduongthucpham.org.vn/index.php/jfns/issue/archive':
                    extract_information_ddvtp(url)
                    export_table_to_csv(DDVTP_Table, 'ddvtp.csv')
                    create_zip_file('ddvtp.csv', 'ddvtp.zip')
                    if create_zip_file('ddvtp.csv', 'ddvtp.zip'):
                        ddvtp_zip_url = 'ddvtp.zip'
                elif url == 'https://tapchinghiencuuyhoc.vn/index.php/tcncyh/issue/archive':
                    extract_information_yhn(url)
                    export_table_to_csv(YHN_Table, 'yhn.csv')
                    create_zip_file('yhn.csv', 'yhn.zip')
                    if create_zip_file('yhn.csv', 'yhn.zip'):
                        yhn_zip_url = 'yhn.zip'
                elif url == 'https://tapchitaimuihong.vn/index.php/tmh/issue/archive':
                    extract_information_tmh(url)
                    export_table_to_csv(TMH_Table, 'tmh.csv')
                    create_zip_file('tmh.csv', 'tmh.zip')
                    if create_zip_file('tmh.csv', 'tmh.zip'):
                        tmh_zip_url = 'tmh.zip'
    return render_template("home.html", tcnk_zip_url=tcnk_zip_url, yhthvb_zip_url=yhthvb_zip_url, ddvtp_zip_url=ddvtp_zip_url, yhn_zip_url=yhn_zip_url, tmh_zip_url=tmh_zip_url)


@app.route('/<filename>')
def serve_zip(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
