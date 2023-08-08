import csv
import requests
from bs4 import BeautifulSoup



def check_links(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        csv_reader = csv.DictReader(file)
        broken_links = []
        not_found_links = []
        for row in csv_reader:
            url = row['book_link']
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 404:
                    broken_links.append(url)
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if "We couldn't find the page you were looking for." in soup.text:
                        not_found_links.append(url)
            except requests.exceptions.RequestException:
                broken_links.append(url)
        return broken_links, not_found_links

broken_links, not_found_links = check_links('new_books_with_descriptions.csv')

print("Broken links:")
for link in broken_links:
    print(link)

print("\nLinks with 'We couldn't find the page you were looking for.':")
for link in not_found_links:
    print(link)
