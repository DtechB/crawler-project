import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import psycopg2
from decouple import config

def database_test():
    try:
        conn = psycopg2.connect(database="alpha", user=config('DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="127.0.0.1",
                                port="5432")
        conn.close()
        return True
    except:
        return False

if database_test():
    conn = psycopg2.connect(database="alpha", user=config(
        'DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="localhost", port="5432")
    cur = conn.cursor()
    print("The connection with the database was established")
else:
    print("The connection with the database could not be established !")

session = requests.Session()
retry = Retry(connect=1, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)

def validate_url(url):
    try:
        session.mount(url, adapter)
        # print(url + " : " + str(session.get(url, timeout=2).status_code))
        return session.get(url).status_code
    except:
        return 0

def set_status_links_in_database(url, status, site_id):
    cur.execute("INSERT INTO api_link (url, status_code , site_id) \
                                              VALUES ('{}', '{}', '{}')".format(url, status, site_id))
    conn.commit()

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

get_pending_sites()
print(pending_sites)

allowed_domains_ready = []
start_urls_ready = []
for i in pending_sites:
    allowed_domains_ready.append(i['url'])
    start_urls_ready.append("https://" + i['url'])

class MySpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = allowed_domains_ready
    start_urls = start_urls_ready

    internal_links = []
    broken_links = []

    def parse(self, response):

        for link in response.css('a::attr(href)').getall():
            url_crawled = ""
            if link != "":
                if link[0] != 'h':
                    url_crawled = self.start_urls[0] + link
                else:
                    url_crawled = link

                if url_crawled.find(self.allowed_domains[0]): # Check contain url string for internal link
                    if self.internal_links.count(url_crawled) == 0: # Check is Exist in the internal link
                        self.internal_links.append(url_crawled)
                validation_url = validate_url(url_crawled)
                if validation_url != 200:
                    if self.broken_links.count(url_crawled) == 0:
                        self.broken_links.append(url_crawled)
                        set_status_links_in_database(url_crawled, validation_url, 1)

        for link in self.internal_links: # Run Crawler for internal links
            for link in response.css('a::attr(href)').getall():
                url_crawled = ""
                if link != "":
                    if link[0] != 'h':
                        url_crawled = self.start_urls[0] + link
                    else:
                        url_crawled = link

                    if url_crawled.find(self.allowed_domains[0]):  # Check contain url string for internal link
                        print(self.internal_links.count(url_crawled))
                        print(self.internal_links)
                        if self.internal_links.count(url_crawled) == 0:  # Check is Exist in the internal link
                            self.internal_links.append(url_crawled) # Add url crawled to internal link
                    validation_url = validate_url(url_crawled)  # Check Validation of link and get status
                    if validation_url != 200:
                        if self.broken_links.count(url_crawled) == 0:
                            self.broken_links.append(url_crawled)
                            set_status_links_in_database(url_crawled, validation_url, 1)


process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(MySpider)
process.start() # The script will block here until the crawling is finished