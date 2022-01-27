#This file contains a script to obtain information from wikipedia and open library from specified authors. At the moment it stores all json and the url from wikipedia because I am not sure what we want to extract yet atm
import json
import time
import requests
import utils
from tqdm import tqdm

book_data = json.load(open("../data/author_novel.json", "r"))
url = "https://openlibrary.org/search/authors.json?q="
open_auth_url = "https://openlibrary.org/authors/"
author_set = set()
author_info = dict()

def checkHtml(html_page, name):
    bad_terms = ["may refer to:", "Wikipedia does not have an article with this exact name"]
    good_terms = [name]
    return utils.checkHtmlBase(good_terms, bad_terms)

def get_open_author_info(the_id):
    specific_author_url = open_auth_url + the_id + ".json"
    utils.getJson(specific_author_url)

try:
    for book in tqdm(book_data):
        author = book["Author"]
        if not author in author_set:
            author_ids = []
            author_info[author] = dict()
            author_set.add(author)
            before = time.time()
            auth_url = url + author
            auth_query_json = utils.getJson(auth_url)
            if auth_query_json and auth_query_json["numFound"] > 0:
                open_author_info = []
                for doc in auth_query_json["docs"]:
                    open_id = doc["key"]
                    open_author_info.append(get_open_author_info(open_id))
                author_info[author]["openLibrary"] = open_author_info

            for permute_url in utils.wikiPermutes(author, ["_(writer)"]):
                data = utils.getHTML(permute_url, check_func=checkHtml())
                if not data["error"]:
                    author_info[author]["wiki"] = linkOrNone
                    break
                    
            else:
                print(f"Could not access page because status code {r.status_code} with author {author}")
            later = time.time()
            time.sleep(max(3 - (later - before), 0))

            #wiki

except KeyboardInterrupt:
    json.dump(author_info, open("../data/author_info.json", "w"))

json.dump(author_info, open("../data/author_info.json", "w"))
