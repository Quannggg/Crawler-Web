from bs4 import BeautifulSoup
import requests


def extract_information(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(
            f"Failed to retrieve the page {url}. Status code: {result.status_code}")
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
        href = a_tag.get('href')
        last_part = href.split('/')[-1]
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

                    # Extract views information
                    views_div = article_soup.find(
                        'div', class_='list-group-item views')
                    views_summary = views_div.find(
                        'strong', text='Số lượt xem tóm tắt').next_sibling.strip()
                    views_pdf = views_div.find(
                        'strong', text='Số lượt xem PDF').next_sibling.strip()

                    doi_div = article_soup.find(
                        'div', class_='list-group-item doi')
                    doi_link = doi_div.find('a')['href']

                    title_div = article_soup.find('div', class_='panel-body')
                    link_title = title_div.find(
                        'a', class_='title').get('href')

                    header_title = article_soup.find(
                        class_='col-md-8 article-details').find('h2').text.strip()
                    author_text = article_soup.find('div', id='authorString').i.get_text(
                        strip=True).split('1,')[0].strip()
                    affiliation_text = article_soup.find(
                        'div', id='authorString').find('span').get_text(strip=True)

                    print('Date Published:', publication_date)
                    print('Abstract Views', views_summary)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_link)
                    print('Title_link:', link_title)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)


url = "https://tcnhikhoa.vn/index.php/tcnk/issue/archive"
extract_information(url)
