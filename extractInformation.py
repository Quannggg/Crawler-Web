from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataBaseModel import Base, TCNK_Table, TMH_Table, YHTHVB_Table, DDVTP_Table, YHN_Table
import csv
import zipfile
import os

engine = create_engine('sqlite:///information.db')
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables in the database
Base.metadata.create_all(engine)


def extract_information_tcnk(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return
    if session.query(TCNK_Table).count() > 0:
        print("TCNK table already has data. Function deactivated.")
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
                    article_soup = BeautifulSoup(
                        article_info.text, "html.parser")

                    date_published_div = article_soup.find(
                        'div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all(
                        'strong')[0].next_sibling.strip()

                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"
                    views_summary = views_summary.replace(":", "")

                    views_pdf = article_soup.find(
                        'strong', text='Số lượt xem PDF')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"
                    views_pdf = views_pdf.replace(":", "")

                    doi_div = article_soup.find(
                        'div', class_='list-group-item doi')
                    doi_link = doi_div.find(
                        'a')['href'] if doi_div and doi_div.find('a') else "N/A"

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get(
                        'href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()

                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split(
                        '1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()

                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(
                        strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(
                        translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

                    tcnk = TCNK_Table(
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

                    session.add(tcnk)
                    session.commit()


# extract_information(url)


def extract_information_yhthvb(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return
    if session.query(TMH_Table).count() > 0:
        print("YHTHVB table already has data. Function deactivated.")
        return

    soup = BeautifulSoup(result.text, 'html.parser')
    media_bodies = soup.find_all('div', {'class': 'issue-summary-body'})
    last_numbers_list = []

    for media_body in media_bodies:
        a_tag = media_body.find('a', {'class': 'title'})
        if a_tag:
            href = a_tag.get('href')
            last_part = href.split('/')[-1]
            last_numbers_list.append(last_part)

    for last_number in last_numbers_list:
        new_url = f"https://jbdmp.vn/index.php/yhthvb/issue/view/{last_number}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_='col-md-12 pl-0')

            for item in items:
                first_href = item.find('a', href=True)['href']
                number = first_href.split('/')[-1]
                final_url = f"https://jbdmp.vn/index.php/yhthvb/article/view/{number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(
                        article_info.text, "html.parser")

                    date_published_div = article_soup.find(
                        'div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all(
                        'strong')[0].next_sibling.strip()

                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"
                    views_summary = views_summary.replace(":", "")

                    views_pdf = article_soup.find(
                        'strong', text='Số lượt xem chi tiết bài báo')
                    if views_pdf is None:
                        views_pdf = article_soup.find(
                            'strong', text='Số lượt xem Chi tiết bài báo')
                        if views_pdf is None:
                            views_pdf = article_soup.find(
                                'strong', text='Số lượt xem bài toàn văn.pdf')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"
                    views_pdf = views_pdf.replace(":", "")

                    doi_div = article_soup.find(
                        'div', class_='list-group-item doi')
                    doi_link = doi_div.find(
                        'a')['href'] if doi_div and doi_div.find('a') else "N/A"

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get(
                        'href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()

                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split(
                        '1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()

                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(
                        strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(
                        translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

                    yhthvb = YHTHVB_Table(
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

                    session.add(yhthvb)
                    session.commit()


# extract_information_yhthvb("https://jbdmp.vn/index.php/yhthvb/issue/archive")


def extract_information_ddvtp(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return
    if session.query(TMH_Table).count() > 0:
        print("DDVTP table already has data. Function deactivated.")
        return

    soup = BeautifulSoup(result.text, 'html.parser')
    media_bodies = soup.find_all('div', {'class': 'issue-summary-body'})
    last_numbers_list = []

    for media_body in media_bodies:
        a_tag = media_body.find('a', {'class': 'title'})
        if a_tag:
            href = a_tag.get('href')
            last_part = href.split('/')[-1]
            last_numbers_list.append(last_part)

    for last_number in last_numbers_list:
        new_url = f"https://tapchidinhduongthucpham.org.vn/index.php/jfns/issue/view/{last_number}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_='col-md-12 pl-0')

            for item in items:
                first_href = item.find('a', href=True)['href']
                number = first_href.split('/')[-1]
                final_url = f"https://tapchidinhduongthucpham.org.vn/index.php/jfns/article/view/{number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(
                        article_info.text, "html.parser")

                    date_published_div = article_soup.find(
                        'div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all(
                        'strong')[0].next_sibling.strip()

                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"
                    views_summary = views_summary.replace(":", "")

                    views_pdf = article_soup.find(
                        'strong', text='Số lượt xem PDF')
                    if views_pdf is None:
                        views_pdf = article_soup.find(
                            'strong', text='Số lượt xem PDF(English)')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"
                    views_pdf = views_pdf.replace(":", "")

                    doi_div = article_soup.find(
                        'div', class_='list-group-item doi')
                    doi_link = doi_div.find(
                        'a')['href'] if doi_div and doi_div.find('a') else "N/A"

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get(
                        'href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()

                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split(
                        '1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()

                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(
                        strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(
                        translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

                    ddvtp = DDVTP_Table(
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

                    session.add(ddvtp)
                    session.commit()


# extract_information_ddvtp("https://tapchidinhduongthucpham.org.vn/index.php/jfns/issue/archive")


def extract_information_yhn(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return
    if session.query(TMH_Table).count() > 0:
        print("YHN table already has data. Function deactivated.")
        return
    soup = BeautifulSoup(result.text, 'html.parser')
    media_bodies = soup.find_all('div', {'class': 'issue-summary media'})
    last_numbers_list = []

    for media_body in media_bodies:
        a_tag = media_body.find('a', {'class': 'title'})
        if a_tag:
            href = a_tag.get('href')
            last_part = href.split('/')[-1]
            last_numbers_list.append(last_part)

    for last_number in last_numbers_list:
        new_url = f"https://tapchinghiencuuyhoc.vn/index.php/tcncyh/issue/view/{last_number}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_='col-md-12')

            for item in items:
                first_href = item.find('a', href=True)['href']
                number = first_href.split('/')[-1]
                final_url = f"https://tapchinghiencuuyhoc.vn/index.php/tcncyh/article/view/{number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(
                        article_info.text, "html.parser")

                    date_published_div = article_soup.find(
                        'div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all(
                        'strong')[0].next_sibling.strip()

                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"
                    views_summary = views_summary.replace(":", "")

                    views_pdf = article_soup.find(
                        'strong', text='Số lượt xem PDF')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"
                    views_pdf = views_pdf.replace(":", "")

                    doi_div = article_soup.find(
                        'div', class_='list-group-item doi')
                    doi_link = doi_div.find(
                        'a')['href'] if doi_div and doi_div.find('a') else "N/A"

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get(
                        'href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()

                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split(
                        '1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()

                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(
                        strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(
                        translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

                    yhn = YHN_Table(
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

                    session.add(yhn)
                    session.commit()


# extract_information_yhn("https://tapchinghiencuuyhoc.vn/index.php/tcncyh/issue/archive")


def extract_information_tmh(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return
    if session.query(TMH_Table).count() > 0:
        print("TMH table already has data. Function deactivated.")
        return
    soup = BeautifulSoup(result.text, 'html.parser')
    media_bodies = soup.find_all('div', {'class': 'issue-summary-body'})
    last_numbers_list = []

    for media_body in media_bodies:
        a_tag = media_body.find('a', {'class': 'title'})
        if a_tag:
            href = a_tag.get('href')
            last_part = href.split('/')[-1]
            last_numbers_list.append(last_part)

    for last_number in last_numbers_list:
        new_url = f"https://tapchitaimuihong.vn/index.php/tmh/issue/view/{last_number}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_='col-md-12 pl-0')

            for item in items:
                first_href = item.find('a', href=True)['href']
                number = first_href.split('/')[-1]
                final_url = f"https://tapchitaimuihong.vn/index.php/tmh/article/view/{number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(
                        article_info.text, "html.parser")

                    date_published_div = article_soup.find(
                        'div', class_='list-group-item date-published')
                    publication_date = date_published_div.find_all(
                        'strong')[0].next_sibling.strip()

                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt')
                    views_summary = views_summary.next_sibling.strip() if views_summary else "N/A"
                    views_summary = views_summary.replace(":", "")

                    views_pdf = article_soup.find(
                        'strong', text='Số lượt xem PDF')
                    views_pdf = views_pdf.next_sibling.strip() if views_pdf else "N/A"
                    views_pdf = views_pdf.replace(":", "")

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find('a', class_='title').get(
                        'href') if title_div and title_div.find('a', class_='title') else "N/A"

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    header_title = header_title.lower()

                    author_div = article_soup.find('div', id='authorString')
                    author_text = author_div.i.get_text(strip=True).split(
                        '1,')[0].strip() if author_div and author_div.i else "N/A"
                    author_text = author_text.lower()

                    affiliation_span = author_div.find('span')
                    affiliation_text = affiliation_span.get_text(
                        strip=True) if affiliation_span else "N/A"
                    translation_table = str.maketrans('', '', '0123456789')
                    affiliation_text = affiliation_text.translate(
                        translation_table).lower()

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('Title Link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

                    tmh = TMH_Table(
                        publication_date=publication_date,
                        views_summary=views_summary,
                        views_pdf=views_pdf,
                        link_title=link_title,
                        header_title=header_title,
                        author_text=author_text,
                        affiliation_text=affiliation_text
                    )

                    # Add the article to the session and commit to the database

                    session.add(tmh)
                    session.commit()


# extract_information_tmh("https://tapchitaimuihong.vn/index.php/tmh/issue/archive")


def export_table_to_csv(table, csv_filename):
    try:
        engine = create_engine('sqlite:///information.db')
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query all records from the specified table
        records = session.query(table).all()

        # Get the table column names
        column_names = [column.name for column in table.__table__.columns]

        # Write data to CSV file
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header row
            csv_writer.writerow(column_names)

            # Write data rows
            for record in records:
                csv_writer.writerow([getattr(record, column)
                                     for column in column_names])

        session.close()
        return True  # Success
    except Exception as e:
        print(f"Error exporting table to CSV: {e}")
        return False  # Failure


def create_zip_file(csv_filename, zip_filename):
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_filename, os.path.basename(csv_filename))
        return True
    except Exception as e:
        print(f"Error creating zip file: {e}")
        return False
