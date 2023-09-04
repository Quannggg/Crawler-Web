from flask import Flask, render_template, request
# from TestCrawl import extract_information

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello world"
    # if request.method == 'POST':
    #     search_term = request.form['search_term']
    #     url = f"https://jiem.ftu.edu.vn/index.php/jiem/issue/archive?q={search_term}"
    #     data = extract_information(url)
    #     return render_template('results.html', data=data, search_term=search_term)
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

