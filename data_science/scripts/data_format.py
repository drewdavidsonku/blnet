import json
from tqdm import tqdm
import sys

all_data = json.load(open('../data/processed_data.json', 'r'))
author_novel = json.load(open('../data/author_novel.json', 'r'))
file_data = json.load(open('../data/BBIP-2021-10.json', 'r'))
book_data = all_data['TITLE_TO_DATA']

title_author = dict()
for data in file_data:
    title_author[data['Title']] = {'author': data['Author'], 'file': data['Filename']}

def unionAll(data_block):
    all_things = set()
    sources_used = set()
    for block in data_block:
        sources_used.add(block['origin'])
        if type(block['value']) == list:
            for block_elem in block['value']:
                all_things.add(block_elem)
        else:
            all_things.add(block['value'])
    all_things = list(all_things)
    if all_things == []:
        return None, None
    return all_things, list(sources_used)

def priorityChoose(data_block):
    priority_sources = ["loc", "google_query", "openlib"]
    best_index = 4
    best_item = None
    best_item_source = None
    for block in data_block:
        if block['origin'] not in priority_sources:
            raise ValueError("Origin not in sources")
        else:
            new_index = priority_sources.index(block['origin'])
            if new_index < best_index:
                best_item = block['value']
                best_item_source = block['origin']
    return best_item, best_item_source

def addSource(all_source, sing_source):
    if sing_source == None or sing_source == []:
        return
    if type(sing_source) == list:
        for s in sing_source:
            all_source.add(s)
    else:
        all_source.add(sing_source)

formatted_data = []
for title in tqdm(book_data):
    ind_book_data = []
    for book in book_data[title]:
        obj = dict()
        all_source = set()
        #subjects
        obj['subjects'], obj['subjects_source'] = unionAll(book['data']['subjects'])
        #genres
        obj['genres'], obj['genres_source'] = unionAll(book['data']['genres'])
        #summary
        obj['summary'], obj['summary_source'] = priorityChoose(book['data']['summary'])
        #author
        obj['author'], obj['author_source'] = priorityChoose(book['data']['author'])
        #locations
        obj['locations'], obj['locations_source'] = unionAll(book['data']['locations'])
        #timePeriod
        obj['timePeriod'], obj['timePeriod_source'] = priorityChoose(book['data']['timePeriod'])
        #publisher
        obj['publisher'], obj['publisher_source'] = priorityChoose(book['data']['publisher'])
        #publishLocation
        obj['publishLocation'], obj['publishLocation_source'] = priorityChoose(book['data']['publishLocation'])
        #rating
        obj['rating'], obj['rating_source'] = priorityChoose(book['data']['rating'])
        #pageCount
        obj['pageCount'], obj['pageCount_source'] = priorityChoose(book['data']['pageCount'])
        #download
        obj['download'], obj['download_source'] = unionAll(book['data']['download'])

        #book date
        if book['data']['publishDate']:
            final_date = -1 * sys.maxsize
            final_source = None
            for dates in book['data']['publishDate']:
                if dates['value'] > final_date:
                    final_date = dates['value']
                    final_source = dates['origin']
            obj['date'] = final_date
            obj['date_source'] = final_source
        else:
            obj['date'] = None
            obj['date_source'] = None

        #setting isbn
        if book["ISBN"]:
            obj['_id'] = book["ISBN"]
        else:
            obj['_id'] = title

        ind_book_data.append(obj)
    formatted_data.append(obj)

isbn_title = []
for t in all_data['TITLE_TO_ISBN']:
    author = "unknown"
    if t in title_author:
        author = title_author[t]['author']
        file = title_author[t]['file']
    isbn_title.append({"_id":t, "ISBN":all_data['TITLE_TO_ISBN'][t], "author":author, 'file':file})

json.dump(formatted_data, open('../data/isbn_data.json', 'w'))
json.dump(isbn_title, open('../data/title_to_isbn.json', 'w'))
