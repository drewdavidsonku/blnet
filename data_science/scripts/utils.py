import requests
import re
from bs4 import BeautifulSoup
import random
import os
import json
import time
import numpy
import unidecode
from tqdm import tqdm

def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]

def LCSubStr(X, Y):
    m = len(X)
    n = len(Y)
    LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]
 
    result = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                LCSuff[i][j] = 0
            elif (X[i-1] == Y[j-1]):
                LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                result = max(result, LCSuff[i][j])
            else:
                LCSuff[i][j] = 0
    return result

def reduceTitle(title):
    title = bytes(title, 'utf-8').decode('utf-8', 'ignore')
    replace_title = title.lower().strip().replace("&", 'and').replace(",", "").replace(';', '').replace(':','').replace('-', '').replace("'", "").replace('"', "").replace('.', '')
    return replace_title

def getRandomSpinner():
    return random.choice(['classic',
                          'stars',
                          'arrows',
                          'arrow',
                          'vertical',
                          'waves',
                          'waves2',
                          'waves3',
                          'horizontal',
                          'dots',
                          'dots_reverse',
                          'dots_waves',
                          'dots_waves2',
                          'ball_scrolling',
                          'balls_scrolling',
                          'ball_bouncing',
                          'balls_bouncing',
                          'dots_recur',
                          'bar_recur',
                          'pointer',
                          'arrows_recur',
                          'triangles',
                          'triangles2',
                          'brackets',
                          'balls_filling',
                          'notes',
                          'notes2',
                          'notes_scrolling',
                          'arrows_incoming',
                          'arrows_outgoing',
                          'real_arrow',
                          'fish',
                          'fish2',
                          'fish_bouncing',
                          'fishes',
                          'pulse'])

def cleanAuthor(author):
    return unidecode.unidecode(author.strip().lower())

def cleanAndNormAuthor(raw_author):
    return cleanAuthor(createAuthorName(raw_author))

def getLastName(raw_author):
#     raw_author = raw_author.replace(" M.D.", "")
#     auth_list = raw_author.split(" ")
#     for auth in auth_list:
#         if auth[-1] == ",":
#             return auth[:-1]
    return createAuthorName(raw_author).split(' ')[-1]

def getFirstName(raw_author):
    return createAuthorName(raw_author).split(" ")[0]

def removeSirNames(author):
    author = author.lower()
    sir_names = ['jr.', 'm.d.', 'j.d.']
    for s in sir_names:
        if s in author:
            author = author.replace(f" {s}", "")
    return author

def createAuthorName(author):
    author = removeSirNames(author)
    auth_list = author.split(" ")
    full_name = ""
    if len(auth_list) == 1:
        return auth_list[0]
    elif len(auth_list) == 2:
        if auth_list[0][-1] == ",":
            full_name = " ".join(auth_list[1:]) + " " + auth_list[0][:-1]
        else:
            return " ".join(auth_list)
    elif len(auth_list) > 2:
        if auth_list[1][-1] == ",":
            full_name = (auth_list[2] + " " + " ".join(auth_list[:2])).replace(",", "").strip()
        elif auth_list[0][-1] == ",":
            full_name = (" ".join(auth_list[1:]) + " " + auth_list[0]).replace(",", "").strip()
        else:
            return " ".join(auth_list)
    return full_name

def getJson(url, wait=0, fail_attempt_num=0, fail_wait=30):
    time.sleep(wait)
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            if r.text:
                try:
                    json_data = json.loads(r.text)
                    return json_data
                except Exception as e:
                    print(e)
                    return None
        elif r.status_code == 429 or r.status_code == 403:
            time.sleep(fail_wait*(restrict_resp_count+1))
            if restrict_resp_count > 4:
                return None
            return getJson(url, fail_attempt_num=fail_attempt_num+1, wait=5)
        else:
            print(f"Returned status code of {r.status_code} with url: {url}")
            return None
    except Exception as e:
        print(e)    
        return None

def checkHtmlBase(good_terms, bad_terms):
    def checkHtmlWrapper(text):
        for term in bad_terms:
            if text.find(term.strip()) > -1:
                return False
        for term in good_terms:
            if text.find(term) == -1:
                return False

        return True
    return checkHtmlWrapper

def getHTML(url, wait=0, fail_wait=5, restrict_count=0, check_func=None):
    try:
        time.sleep(wait)
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            if check_func and check_func(r.text):
                return {"url": url, "html": r.text, "error": None}
            elif not check_func:
                return {"url":url, "html": r.text, "error": None}
            return {"url": url, "html": r.text, "error": "Did not pass check function"}
        elif r.status_code == 429:
            if restrict_count > 4:
                return {"url": url, "html": None, "error": f"Response code {r.status_code}"}
            time.sleep(fail_wait * (restrict_count + 1))
            return getHTML(url, fail_wait, restrict_count + 1, check_func)

        elif r.status_code != 200 and r.status_code != 429:
            return {"url": url, "html": None, "error": f"Response code {r.status_code}"}
        else:
            return {"url": url, "html": None, "error": f"Response code {r.status_code}"}
    except Exception as e:
        print(e)
        return {"url": url, "html": None, "error": "Timeout"}

def wikiPermutes(main_query, permutes):
    base_url = "https://en.wikipedia.org/wiki/"
    all_permutes = []

    all_permutes.append(base_url + main_query)
    for p in permutes:
        all_permutes.append(base_url + main_query + p)

    return all_permutes

def getOcrIsbn():
    all_isbns = dict()
    ocr_json_data = json.load(open('../data/BBIP-2021-10.json', 'r'))

    for ocr_book_data in tqdm(ocr_json_data):
        temp_isbn = getIsbnFromFile(ocr_book_data["Filename"])
        if temp_isbn != None:
            for isbn in temp_isbn:
                all_isbns[isbn] = ocr_book_data['Title']
    return all_isbns

ISBN_REGEX = re.compile(r'isbn(?:-13)?:?[^\S\r\n]*([\d-]{10,18})', re.IGNORECASE)
def getIsbnFromFile(file_name):
    full_path = os.path.join('../data/ocr_book/', str(file_name) + '.htm')
    try:
        with open(full_path, 'r') as f:
            raw_html = f.read()
            content_soup = BeautifulSoup(raw_html)
            content = content_soup.get_text()
            re_match = ISBN_REGEX.findall(content)
            if re_match:
                lis_isbn = list(set([m.replace('-', '') for m in re_match if len(m.replace('-', '')) == 13]))
                if len(lis_isbn) > 0:
                    return lis_isbn
            return None
    except FileNotFoundError:
        print(f'File not found for {str(file_name) + ".htm"}')
        return None
