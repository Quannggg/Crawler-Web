from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///information.db')
Session = sessionmaker(bind=engine)
session = Session()
# Define the database model
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)

# Create the tables in the database
Base.metadata.create_all(engine)

def extract_information(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return

    soup = BeautifulSoup(result.text, 'html.parser')
    media_bodies = soup.find_all('div', {'class': 'media-body'})
    last_numbers_list = []

    for media_body in media_bodies:
        a_tag = media_body.find('a', {'class': 'title'})
        if a_tag:
            href = a_tag.get('href')
            last_part = href.split('/')[-1]
            last_numbers_list.append(last_part)
    
    for last_number in last_numbers_list:
        new_url = f"https://tcnhikhoa.vn/index.php/tcnk/issue/view/{last_number}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_='col-md-12')

            for item in items:
                first_href = item.find('a', href=True)['href']
                number = first_href.split('/')[-1]
                final_url = f"https://tcnhikhoa.vn/index.php/tcnk/article/view/{number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(article_info.text, "html.parser")

                    date_published_div = article_soup.find('div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all('strong')[0].next_sibling.strip()

                    views_div = article_soup.find('div', class_='list-group-item views')
                    views_summary = views_div.find('strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"

                    views_pdf = article_soup.find('strong', text='Số lượt xem PDF')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"

                    doi_div = article_soup.find('div', class_='list-group-item doi')
                    doi_link = doi_div.find('a')['href'] if doi_div and doi_div.find('a') else "N/A"

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get('href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()
                    
                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split('1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()
                    
                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)
                    
                    article = Article(
                        publication_date=publication_date,
                        views_summary=views_summary,
                        views_pdf=views_pdf,
                        doi_link=doi_link,
                        link_title=link_title,
                        header_title=header_title,
                        author_text=author_text,
                        affiliation_text=affiliation_text
                    )

                    # Add the article to the session and commit to the database
                    views_summary = views_summary.replace(":", "")
                    views_pdf = views_pdf.replace(":", "")
                    session.add(article)
                    session.commit()

url = "https://tcnhikhoa.vn/index.php/tcnk/issue/archive"
extract_information(url)
