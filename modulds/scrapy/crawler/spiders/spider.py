# Import required libraries
import scrapy
import psycopg2
from decouple import config
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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


# Define variables
links_array = []
internal_links = []
broken_link_list = []
checked_before = []

# Get URL and Level of crawling
crawl_level = 2
url_input = sys.argv[5].split('=')[1]

start_url_maker = "https://" + url_input + "/"

# Function for Fetch URLs that checked before in database
urls = []

# Database connection


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

# This function is currently not available


def add_link_to_database(link, site_id):
    cur.execute("INSERT INTO api_link (url, status_code , site_id) \
                                              VALUES ('{}', '{}', '{}')".format(link, 1, site_id))
    conn.commit()



def validate_url(url):
    session = requests.Session()
    retry = Retry(connect=1, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    try:
        session.mount(url, adapter)
        # print(url + " : " + str(session.get(url, timeout=2).status_code))
        return session.get(url, timeout=2).status_code
    except:
        return 0


def set_status_links_in_database(url, status, site_id):
    cur.execute("INSERT INTO api_link (url, status_code , site_id) \
                                              VALUES ('{}', '{}', '{}')".format(url, status, site_id))
    conn.commit()


def save_in_database(link):
    # Check Validation of link and get status
    validation_url = validate_url(link)
    if validation_url == 200:
        print(bcolors.OKGREEN + "link " + link + " is: " + str(validation_url) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "link " + link + " is: " + str(validation_url) + bcolors.ENDC)
    set_status_links_in_database(link, validation_url, site_id)


site_id = sys.argv[3].split('=')[1]


class Spider(scrapy.Spider):
    print(bcolors.OKBLUE + "--- Spider crawler " +
          url_input + " Started ---" + bcolors.ENDC)
    name = "spider"

    global allowed_domains
    allowed_domains = [url_input]
    start_urls = [
        start_url_maker
    ]

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if link != "":
                if link[0] == 'h':
                    if link not in links_array:
                        links_array.append(link)
                        print(bcolors.OKCYAN + link + bcolors.ENDC)
                        if link.find(allowed_domains[0]) != -1:
                            internal_links.append(link)
                else:
                    full_url_string = self.start_urls[0][:-1] + link
                    if full_url_string not in links_array:
                        links_array.append(full_url_string)
                        print(bcolors.OKCYAN + full_url_string + bcolors.ENDC)
                        if full_url_string.find(allowed_domains[0]) != -1:
                            internal_links.append(full_url_string)

        for k in range(0, crawl_level):
            for internal_link in internal_links:
                if checked_before.count(internal_link) == 0:
                    checked_before.append(internal_link)
                    save_in_database(internal_link)
                    yield scrapy.Request(url=internal_link, callback=self.parse)

