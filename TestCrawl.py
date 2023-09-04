from bs4 import BeautifulSoup
import requests

def extract_information(url):
    result = requests.get(url)
    if result.status_code != 200:
        print(f"Failed to retrieve the page {url}. Status code: {result.status_code}")
        return

    soup = BeautifulSoup(result.text, 'html.parser')
    a_tags = soup.find_all('a', {'class': 'cover'})

    for a_tag in a_tags:
        href = a_tag.get('href')
        last_part = href.split('/')[-1]
        new_url = f"https://jiem.ftu.edu.vn/index.php/jiem/issue/view/{last_part}"
        issue_info = requests.get(new_url)

        if issue_info.status_code == 200:
            issue_soup = BeautifulSoup(issue_info.text, "html.parser")
            items = issue_soup.find_all(class_="col-md-12 pl-0")
            
            for item in items:
                first_href = item.find('a', href=True)['href']
                last_number = first_href.split('/')[-1]
                final_url = f"https://jiem.ftu.edu.vn/index.php/jiem/article/view/{last_number}"
                article_info = requests.get(final_url)

                if article_info.status_code == 200:
                    article_soup = BeautifulSoup(article_info.text, "html.parser")
                    
                    date_published = article_soup.find('div', class_='date-published').get_text(strip=True).replace('Date Published:', '')
                    abstract_views = article_soup.find('strong', string='Abstract Views').next_sibling.strip()
                    views_pdf = article_soup.find('strong', string='Views PDF').next_sibling.strip()
                    doi_value = article_soup.find('div', class_='list-group-item doi').find('a')['href']
                    title_value = article_soup.find('div', class_='panel-body').find('a')['href']
                    header_title = article_soup.find(class_='col-md-8 article-details').find('h2').text.strip()
                    author_text = article_soup.find('div', id='authorString').i.get_text(strip=True).split('1,')[0].strip()
                    affiliation_text = article_soup.find('div', id='authorString').find('span').get_text(strip=True)

                    print('Date Published:', date_published)
                    print('Abstract Views', abstract_views)
                    print('Views PDF', views_pdf)
                    print('DOI:', doi_value)
                    print('Title_link:', title_value)
                    print('Title:', header_title)
                    print("Author's Name:", author_text)
                    print("Affiliation:", affiliation_text)
                    print('-' * 50)

url = "https://jiem.ftu.edu.vn/index.php/jiem/issue/archive"
extract_information(url)
