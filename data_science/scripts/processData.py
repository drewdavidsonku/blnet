import utils
from datetime import datetime
import json
from alive_progress import alive_bar
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        time = parse(string, fuzzy=fuzzy)
        return time.timestamp()

    except ValueError:
        return False

GOOGLE_QUERY_DATA = json.load(open('../data/google_query_data.json', 'r'))
LOC_DATA = json.load(open('../data/loc_data.json', 'r'))
OPENLIB_DATA = json.load(open('../data/openlib_data.json', 'r'))

# template
# dict(
#   (isbn)-String: list(
#     dict(
#       title
#       author
#       summary
#       subjects
#       locations
#       genres
#       timePeriod
#       publisher
#       publishLocation
#       publishDate
#       rating
#       pageCount
#     )
#   )
# )

metadata_topics = ["title", "author", "summary", "subjects", "locations", "genres",\
        "timePeriod", "publisher", "publishLocation", "publishDate", "rating", "pageCount"]

def loc_data_extract(data_dict, raw_data):
    for t in metadata_topics:
        if t in raw_data and raw_data[t]:
            if t == "publishDate":
                store_val = is_date(raw_data[t])
                if store_val != False:
                    data_dict[t].append({"origin": "loc", "value": store_val})
            else:
                data_dict[t].append({"origin": "loc", "value": raw_data[t]})

def openlib_data_extract(data_dict, raw_data):
    if "publishers" in raw_data and raw_data["publishers"]:
        data_dict["publisher"].append({"origin": "openlib", "value": raw_data["publishers"]})
    if "number_of_pages" in raw_data and raw_data["number_of_pages"]:
        data_dict["pageCount"].append({"origin": "openlib", "value": raw_data["number_of_pages"]})
    if "subjects" in raw_data and raw_data["subjects"]:
        data_dict["subjects"].append({"origin": "openlib", "value": raw_data["subjects"]})
    if "title" in raw_data and raw_data["title"]:
        data_dict["title"].append({"origin": "openlib", "value": raw_data["title"]})
    if "publish_date" in raw_data and raw_data["publish_date"]:
        store_val = is_date(raw_data["publish_date"])
        if store_val != False:
            data_dict["publishDate"].append({"origin": "openlib", "value": store_val})
    if "description" in raw_data and raw_data["description"] and \
            "value" in raw_data['description'] and raw_data['description']['value']:
        data_dict["summary"].append({"origin": "openlib", "value": raw_data["description"]['value']})

def google_query_data_extract(data_dict, raw_data):
    if 'volumeInfo' in raw_data:
        info = raw_data['volumeInfo']
        if 'title' in info:
            data_dict['title'].append({'origin': 'google_query', 'value': info['title']})
        if 'publisher' in info:
            data_dict['publisher'].append({'origin': 'google_query', 'value': info['publisher']})
        if 'publishedDate' in info:
            store_val = is_date(info['publishedDate'])
            if store_val != False:
                data_dict['publishDate'].append({'origin': 'google_query', 'value': store_val})
        if 'pageCount' in info:
            data_dict['pageCount'].append({'origin': 'google_query', 'value': info['pageCount']})
        if 'categories' in info:
            data_dict['subjects'].append({'origin': 'google_query', 'value': info['categories']})
        if 'averageRating' in info:
            data_dict['rating'].append({'origin': 'google_query', 'value': info['averageRating']})
    if "accessInfo" in raw_data:
        access_info = raw_data["accessInfo"]
        if "pdf" in access_info and "acsTokenLink" in access_info['pdf']:
            data_dict['download'].append({'origin': 'google_query', 'value': access_info['pdf']['acsTokenLink']})
        if "epub" in access_info and "acsTokenLink" in access_info['epub']:
            data_dict['download'].append({'origin': 'google_query', 'value': access_info['epub']['acsTokenLink']})

COMBINED_QUERY_DATA = dict()

#combine the different sources together
with alive_bar(len(list(GOOGLE_QUERY_DATA["ISBN_TO_TITLE"].keys())), spinner=utils.getRandomSpinner()) as bar:
    for isbn in GOOGLE_QUERY_DATA["ISBN_TO_TITLE"]:
        bar()
        isbn_dict = {
            "title": [],
            "author": [],
            "summary": [],
            "subjects": [],
            "locations": [],
            "genres": [],
            "timePeriod": [],
            "publisher": [],
            "publishLocation": [],
            "publishDate": [],
            "rating": [],
            "pageCount": [],
            "download": []
                }
        if isbn in LOC_DATA:
            loc_data_extract(isbn_dict, LOC_DATA[isbn]) 
        if isbn in OPENLIB_DATA:
            openlib_data_extract(isbn_dict, OPENLIB_DATA[isbn])
        if isbn in GOOGLE_QUERY_DATA["ISBN_DATA"]:
            google_query_data_extract(isbn_dict, GOOGLE_QUERY_DATA["ISBN_DATA"][isbn])
        COMBINED_QUERY_DATA[isbn] = isbn_dict
            
#combine isbn to title
TITLE_TO_ISBN = dict()
with alive_bar(len(list(GOOGLE_QUERY_DATA["ISBN_TO_TITLE"].keys())), spinner=utils.getRandomSpinner()) as bar:
    for isbn in GOOGLE_QUERY_DATA["ISBN_TO_TITLE"]:
        bar()
        if not GOOGLE_QUERY_DATA["ISBN_TO_TITLE"][isbn] in TITLE_TO_ISBN:
            TITLE_TO_ISBN[GOOGLE_QUERY_DATA["ISBN_TO_TITLE"][isbn]] = [isbn]
        else:
            TITLE_TO_ISBN[GOOGLE_QUERY_DATA["ISBN_TO_TITLE"][isbn]].append(isbn)

TITLE_TO_DATA = dict()
with alive_bar(len(list(TITLE_TO_ISBN.keys())), spinner=utils.getRandomSpinner()) as bar:
    for title in TITLE_TO_ISBN:
        bar()
        for isbn in TITLE_TO_ISBN[title]:
            if isbn in COMBINED_QUERY_DATA:
                if not title in TITLE_TO_DATA:
                    TITLE_TO_DATA[title] = [{"ISBN": isbn, "data": COMBINED_QUERY_DATA[isbn]}]
                else:
                    TITLE_TO_DATA[title].append({"ISBN": isbn, "data": COMBINED_QUERY_DATA[isbn]})

with alive_bar(len(list(GOOGLE_QUERY_DATA['NO_ISBN_DICT'].keys())), spinner=utils.getRandomSpinner()) as bar:
    for title in GOOGLE_QUERY_DATA['NO_ISBN_DICT']:
        bar()
        title_data = GOOGLE_QUERY_DATA['NO_ISBN_DICT'][title]
        if not title in TITLE_TO_DATA:
            TITLE_TO_DATA[title] = []
        for data in title_data:
            isbn_dict = {
                "title": [],
                "author": [],
                "summary": [],
                "subjects": [],
                "locations": [],
                "genres": [],
                "timePeriod": [],
                "publisher": [],
                "publishLocation": [],
                "publishDate": [],
                "rating": [],
                "pageCount": [],
                "download": []
                    }
            google_query_data_extract(isbn_dict, data)
            TITLE_TO_DATA[title].append({"ISBN": None, "data": isbn_dict})

PROCESSED_DATA = {
            "TITLE_TO_ISBN": TITLE_TO_ISBN,
            "TITLE_TO_DATA": TITLE_TO_DATA
        }

json.dump(PROCESSED_DATA, open("../data/processed_data.json", "w"))
