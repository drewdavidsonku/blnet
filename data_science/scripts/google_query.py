import utils
import json
from alive_progress import alive_bar
import xml.etree.cElementTree as ET

SAVE_DATA = True 

DO_GOOGLE_QUERY = True
DO_GOOGLE_ISBN = True
DO_OPENLIB_ISBN = True
DO_LOC_ISBN = True

RELOAD_LOC_DATA = False 

BASE_GOOGLE_URL = "https://www.googleapis.com/books/v1/volumes?q=intitle:"
OPENLIB_URL = "https://openlibrary.org/isbn/"
book_data = json.load(open("../data/author_novel.json", "r"))

def make_google_url(sing_book_data):
    title = sing_book_data["Title"].replace(" ", "+")
    author = sing_book_data["Author"]
    full_name = utils.createAuthorName(author).replace(" ", "+")
    base_url = f'{BASE_GOOGLE_URL}"{title}"+inauthor:"{full_name}"'
    return base_url

def getGoogleJson(goog_url):
    perlim_json = utils.getJson(goog_url, wait=0.5)
    if perlim_json:
        if "totalItems" in perlim_json:
            if perlim_json['totalItems'] > 0:
                return perlim_json
    return None

def removeAuthorInUrl(url, with_key=True):
    begin_index = url.find("+inauthor:")
    end_index = url.find("&key=")
    if not with_key:
        return url[:begin_index]
    return url[:begin_index] + url[end_index:]

def findISBN(data_block):
    if 'industryIdentifiers' in data_block['volumeInfo']:
        for identify in data_block['volumeInfo']['industryIdentifiers']:
            if identify['type'] == "ISBN_13":
                return identify['identifier']
    return None

def checkTitle(resp_title, real_title):
    our_reduced_title = utils.reduceTitle(title)
    google_reduced_title = utils.reduceTitle(resp_title)
    if (our_reduced_title.find(google_reduced_title) > -1 or \
            google_reduced_title.find(our_reduced_title) > -1) and \
            utils.levenshteinDistanceDP(our_reduced_title, google_reduced_title) < 3:
        return True
    return False

def checkAuthor(resp_author, real_author):
    if real_author == "unknown":
        return True
    norm_resp_author = utils.cleanAndNormAuthor(resp_author)
    last_name_real = utils.cleanAuthor(utils.getLastName(real_author))
    first_name_real = utils.cleanAuthor(utils.getFirstName(real_author))
    if norm_resp_author.find(last_name_real) > -1 or\
            len(last_name_real) - utils.LCSubStr(norm_resp_author, last_name_real) < 2:
        return True
    return False

def checkBookResponse(data_block, title, author):
    if not 'volumeInfo' in data_block or not "title" in data_block['volumeInfo'] or \
        not 'authors' in data_block['volumeInfo']:
        return False
    google_title = item['volumeInfo']['title']
    google_author = item['volumeInfo']['authors'][0]
    if checkTitle(google_title, title):
        if not checkAuthor(google_author, author):
            return False
        else:
            return True
    return False

def LOC_URL(isbn):
    return f"http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn={isbn}&maximumRecords=1&recordSchema=mods"

def xmlString(query, mod):
    if mod:
        return f"{{http://www.loc.gov/mods/v3}}{query}"
    return f"{{http://www.loc.gov/zing/srw/}}{query}"

def xmlFindWrapper(element):
    if element != None:
        return element.text
    return None


ISBN_TO_TITLE = utils.getOcrIsbn()
ISBN_DATA = dict()
NO_ISBN_DICT = dict()

if DO_GOOGLE_QUERY:
    try:
        with alive_bar(len(book_data), spinner=utils.getRandomSpinner()) as bar:
            for book in book_data:
                bar()

                google_url = make_google_url(book)
                author = book["Author"]
                title = book["Title"]

                google_book_json = getGoogleJson(google_url)
                if google_book_json == None:
                    google_book_json = getGoogleJson(removeAuthorInUrl(google_url))

                if google_book_json != None and len(google_book_json['items']) > 0:
                    for item in google_book_json['items']:
                        if checkBookResponse(item, title, author):
                            isbn = findISBN(item)
                            if isbn == None:
                                if not title in NO_ISBN_DICT:
                                    NO_ISBN_DICT[title] = [item]
                                else:
                                    NO_ISBN_DICT[title].append(item)
                            else:
                                ISBN_TO_TITLE[isbn] = title
                                ISBN_DATA[isbn] = item

    except KeyboardInterrupt:
        print("quitting...")
    big_dict = {
            "ISBN_TO_TITLE": ISBN_TO_TITLE,
            "ISBN_DATA":ISBN_DATA,
            "NO_ISBN_DICT":NO_ISBN_DICT
            }

    if SAVE_DATA:
        json.dump(big_dict, open("../data/google_query_data.json", "w"))
else:
    big_dict = json.load(open("../data/google_query_data.json", "r"))

OPENLIB_DICT = dict()

if DO_OPENLIB_ISBN:
    with alive_bar(len(list(big_dict['ISBN_TO_TITLE'].keys())), spinner=utils.getRandomSpinner()) as bar:
        for isbn in big_dict['ISBN_TO_TITLE']:
            bar()

            openlib_url = OPENLIB_URL + str(isbn) + ".json"
            prelim_json = utils.getJson(openlib_url, wait=1)
            if prelim_json != None:
                OPENLIB_DICT[isbn] = prelim_json

    if SAVE_DATA:
        json.dump(OPENLIB_DICT, open('../data/openlib_data.json', 'w')) 

LOC_ISBN = dict()
if RELOAD_LOC_DATA:
    print("reloading...")
    LOC_ISBN = json.load( open("../data/loc_data.json", 'r'))
    print(f"previous data from LOC of {len(list(LOC_ISBN.keys()))} pieces of data")
if DO_LOC_ISBN:
    try:
        with alive_bar(len(list(big_dict['ISBN_TO_TITLE'].keys())), spinner=utils.getRandomSpinner()) as bar:
            for isbn in big_dict['ISBN_TO_TITLE']:
                bar()
                if not isbn in LOC_ISBN:
                    loc_url = LOC_URL(isbn)
                    html_data = utils.getHTML(loc_url, wait=5)
                    if not html_data["error"]:
                        xml = ET.fromstring(html_data['html'])
                        recordQuery = xml.find(xmlString("numberOfRecords", False))
                        if recordQuery != None:
                            records = int(xml.find(xmlString("numberOfRecords", False)).text)
                            if records > 0:
                                titleString = xmlString("title", True)
                                authorString = xmlString("namePart", True)
                                descriptionString = xmlString("abstract", True)
                                subjectString = xmlString("topic", True)
                                geoString = xmlString("geographic", True)
                                genreString = xmlString("genre", True)
                                temporalString = xmlString("temporal", True)
                                publisherString = xmlString("publisher", True)
                                publishLocString = xmlString("placeTerm", True)
                                publishDateString = xmlString("dateIssued", True)

                                title = xmlFindWrapper(xml.find(".//" + titleString))
                                author = xmlFindWrapper(xml.find(".//" + authorString))
                                description = xmlFindWrapper(xml.find(descriptionString))
                                subjectElements = xml.findall('.//' + subjectString)
                                subjects = [x.text for x in subjectElements if x != None]
                                geoElements = xml.findall('.//' + geoString)
                                geos = [x.text for x in geoElements]
                                genreElements = xml.findall('.//' + genreString)
                                genres = list(set([x.text for x in genreElements if x != None]))
                                temporal = xmlFindWrapper(xml.find('.//' + temporalString))

                                publisher = xmlFindWrapper(xml.find('.//' + publisherString))
                                publishLocElements = xml.findall('.//' + publishLocString)
                                publishLoc = [x.text for x in publishLocElements if x != None]
                                publishDate = xmlFindWrapper(xml.find('.//' + publishDateString))

                                isbnDict = {
                                        "title": title,
                                        "author": author,
                                        "summary": description,
                                        "subjects": subjects,
                                        "locations": geos,
                                        "genres": genres,
                                        "timePeriod": temporal,
                                        "publisher": publisher,
                                        "publishLocation": publishLoc,
                                        "publishDate": publishDate
                                        }

                                LOC_ISBN[isbn] = isbnDict
    except KeyboardInterrupt:    
        if SAVE_DATA:
            json.dump(LOC_ISBN, open("../data/loc_data.json", "w"))
