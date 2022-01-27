import json
import re
import utils
import requests
import os
from tqdm import tqdm

processed_data = json.load(open('../data/processed_data.json', 'r'))['TITLE_TO_DATA']
ocr_books_json = json.load(open('../data/ocr_author_novel.json', 'r'))

download_books = dict()
ocr_books = set()
new_pdf_books = set()

for book in tqdm(processed_data):
    for isbn_book in processed_data[book]:
        if isbn_book['data']['download']:
            dir_path = f'./pdf_epubs/{book}'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            for link in isbn_book['data']['download']:
                filename = f"./pdf_epubs/{book}/{link['value'].split('/')[-1]}" 
                r = requests.get(link['value'], allow_redirects=True)

                with open(filename,'wb') as output_file:
                    content = r.content
                    match = re.search(b'\"(.*?\.epub)\"', content)
                    if match:
                        print(match.group(1))
                        exit()
                    output_file.write(content)

exit()
for book_data in ocr_books_json:
    ocr_books.add(book_data['Title'])

for book in download_books:
    if not book in ocr_books:
        new_pdf_books.add(book)

print((new_pdf_books))


