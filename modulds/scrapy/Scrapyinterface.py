import os, sys
import psycopg2
from decouple import config

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def database_test():
    try:
        conn = psycopg2.connect(database="alpha", user=config('DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="127.0.0.1",
                                port="5432")
        conn.close()
        return True
    except:
        return False

if database_test():
    conn = psycopg2.connect(database="alpha", user=config('DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="127.0.0.1",
                            port="5432")
    cur = conn.cursor()
    print(bcolors.OKGREEN +
          "The connection with the database was established" + bcolors.ENDC)
else:
    print(bcolors.FAIL +
          "The connection with the database could not be established !" + bcolors.ENDC)
    
pending_sites = []

def get_pending_sites():
    cur.execute("SELECT id, url, status from api_site")
    rows = cur.fetchall()
    for row in rows:
        if row[2] == 'P':
            pending_element = {}
            pending_element.update({"id": row[0]})
            pending_element.update({"url": row[1]})
            pending_element.update({"status": row[2]})
            pending_sites.append(pending_element)

def runCrawler():
    if os.listdir().count("Scrapyinterface.py") != 1:
        os.chdir('./modulds')
        os.chdir('./scrapy')
    print("Start")
    get_pending_sites()
    for i in pending_sites:
        os.system('scrapy crawl spider -a id=' + str(i['id']) + ' -a url=' + i['url'])


runCrawler()