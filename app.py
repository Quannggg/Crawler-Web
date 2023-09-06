from flask import Flask, render_template, request
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from dataBaseModel import Article,Base  

app = Flask(__name__)

# Configure the database connection
db_engine = create_engine('sqlite:///information.db')
Session = sessionmaker(bind=db_engine)

@app.route('/', methods=['POST', 'GET'])
def Scrawl():
    if request.method == 'POST':
        search = request.form.get('search')  # Use 'search' as the form field name
        print(search)
        
        if search:
            session = Session()
            articles = []

            # Get the list of column names in the Article model
            mapper = inspect(Article)
            print(mapper)
            columns = [c.key for c in mapper.attrs]
            print(columns)

            # Create a list of conditions to search across all columns
            search_conditions = [getattr(Article, col).like(f'%{search}%') for col in columns]
            print(search_conditions)

            # Combine conditions with OR to search in any column
            query_condition = or_(*search_conditions)
            print(query_condition)

            # Perform the query using the combined condition
            articles = session.query(Article).filter(query_condition).all()
            # print(articles)

            return render_template("home.html", articles=articles, search=search)
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
