import utils
import json
import os
import csv
from tqdm import tqdm

isbn_data = json.load(open("../data/isbn_to_data.json", "r"))
google_data = json.load(open("../data/google_data.json", "r"))
book_index = json.load(open("../data/author_novel.json", "r"))

book_set = set()
for book in book_index:
    book_set.add(book["Title"])

counts = {
        "summary": 0,
        "publisher": 0,
        "published_date": 0,
        "page_count": 0,
        "category": 0,
        "rating": 0,
        }

ISBN_columns = ["ISBN"] + list(counts.keys())
Query_columns = ["Title"] + list(counts.keys())

isbn_csv_rows = []
query_csv_rows = []
print(f"Info for the isbn data out of {len(list(isbn_data.keys()))} of pieces of data")


for isbn in tqdm(isbn_data):
    sets = {
            "summary": False,
            "publisher": False,
            "published_date": False,
            "page_count": False,
            "category": False,
            "rating": False,
            }
    #summary
    if isbn_data[isbn]['openlib'] and \
            "description" in isbn_data[isbn]['openlib'] and \
            isbn_data[isbn]['openlib']['description'] and \
            'value' in isbn_data[isbn]['openlib']['description'] and \
            isbn_data[isbn]['openlib']['description']['value']:
                sets['summary'] = True

    elif isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('description', None):
        sets['summary'] = True

    #publiehr
    if isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('publisher', None):
        sets['publisher'] = True

    #publish date
    if isbn_data[isbn]['openlib'] and \
            "publish_date" in isbn_data[isbn]['openlib'] and \
            isbn_data[isbn]['openlib']['publish_date']:
        sets['published_date'] = True

    elif isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('publishedDate', None):
        sets['published_date'] = True
    #page count
    if isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('pageCount', None):
        sets['page_count'] = True

    elif isbn_data[isbn]['openlib'] and \
            "number_of_pages" in isbn_data[isbn]['openlib'] and \
            isbn_data[isbn]['openlib']['number_of_pages']:
        sets['page_count'] = True

    #category
    if isbn_data[isbn]['openlib'] and \
            "subjects" in isbn_data[isbn]['openlib'] and \
            isbn_data[isbn]['openlib']['subjects']:
        sets['category'] = True
    
    elif isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('categories', None):
        sets['category'] = True

    #rating
    if isbn_data[isbn].get('google', dict()).get('items', [dict()])[0].get('volumeInfo', dict()).get('averageRating', None):
        sets['rating'] = True

    for tag in sets:
        if sets[tag]:
            counts[tag] += 1

    sets["ISBN"] = isbn
    isbn_csv_rows.append(sets)

print(counts)
with open("../data/csv/isbn_bin_matrix.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=ISBN_columns)
    writer.writeheader()
    writer.writerows(isbn_csv_rows)

counts = {
        "summary": 0,
        "publisher": 0,
        "published_date": 0,
        "page_count": 0,
        "category": 0,
        "rating": 0,
        }

print(f"Info on the queried data out of {len(list(google_data.keys()))} pieces of data")
for query in tqdm(google_data):
    bools = {
            "summary": False,
            "publisher": False,
            "published_date": False,
            "page_count": False,
            "category": False,
            "rating": False,
            }
    title = ""
    if google_data[query] and 'items' in google_data[query] and \
            len(google_data[query]['items']) > 0:
        title = google_data[query]['items'][0]['volumeInfo']['title']
        for book in google_data[query]['items']:
            
            if 'volumeInfo' in book and \
                book['volumeInfo'] :

            #rating
                if 'averageRating' in book['volumeInfo'] and \
                    book['volumeInfo']['averageRating']:

                    bools['rating'] = True

            #category
                if 'categories' in book['volumeInfo'] and \
                    book['volumeInfo']['categories']:
                    
                    bools['category'] = True

            #page count
                if 'pageCount' in book['volumeInfo'] and \
                    book['volumeInfo']['pageCount']:
                    
                    bools['page_count'] = True

            #summary
                if 'description' in book['volumeInfo'] and \
                    book['volumeInfo']['description']:
                    
                    bools['summary'] = True

            #publiehr
                if 'publisher' in book['volumeInfo'] and \
                    book['volumeInfo']['publisher']:
                    
                    bools['publisher'] = True

            #publish date
                if 'publishedDate' in book['volumeInfo'] and \
                    book['volumeInfo']['publishedDate']:
                    
                    bools['published_date'] = True

    for tag in bools:
        if bools[tag]:
            counts[tag] += 1

    bools["Title"] = title
    query_csv_rows.append(bools)


with open("../data/csv/query_bin_matrix.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=Query_columns)
    writer.writeheader()
    writer.writerows(query_csv_rows)

print(counts)
