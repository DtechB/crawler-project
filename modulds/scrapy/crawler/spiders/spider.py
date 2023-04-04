# Import required libraries
import scrapy
import validators
import psycopg2
from anytree import Node, RenderTree

# Define variables
links_array = []
internal_links = []
broken_link_list = []

# Get URL and Level of crawling
# url_input = input("Enter URL to crawling: ")
crawl_level = int(input("Enter Level of Crawling (set 0 for crawl just first page): "))

#url_input = "cert.shahroodut.ac.ir"
    
start_url_maker = "https://" + url_input + "/"
crawl_level = 1

root = Node("Site")
first_depth = []
second_depth = []
third_depth = []
fourth_depth = []
fifth_depth = []
sixth_depth = []
seventh_depth = []
eighth_depth = []
first_depth_tree = []
second_depth_tree = []
third_depth_tree = []
fourth_depth_tree = []
fifth_depth_tree = []
sixth_depth_tree = []


# Check connection with database
def postgres_test():
    try:
        conn = psycopg2.connect(database="Alpha", user="postgres", password="123", host="127.0.0.1",
                                port="5432")
        conn.close()
        return True
    except:
        return False


""" Connect to database
 Database is postgressSQL """
conn = psycopg2.connect(database="Alpha", user="postgres", password="123", host="localhost", port="5432")
cur = conn.cursor()


# Fetch broken links
def FetchBrokenLinks():
    cur.execute("SELECT id, site_url, broken_link from api_brokenUrls")
    rows = cur.fetchall()
    for row in rows:
        broken_link_list.append(row[2])


# Add broken URLs in database
def AddBrokenURLs(broken_link):
    if broken_link not in broken_link_list:
        broken_link_list.append(broken_link)
        cur.execute("INSERT INTO api_brokenUrls (site_url, broken_link) \
                                                  VALUES ('{}', '{}')".format(start_url_maker, broken_link))
        conn.commit()


# Check validation of each url with validation library
def CheckValidation(url):
    validation = validators.url(url, public=True)
    if validation:
        return ("URL is valid")
    else:
        AddBrokenURLs(url)
        return ("URL is invalid")


# Function for Fetch URLs that checked before in database
urls = []
hits_url = []


def FetchUrls():
    cur.execute("SELECT id, url, hits, broken_links_num from api_urlchecked")
    rows = cur.fetchall()
    for row in rows:
        urls.append(row[1])
        hits_url.append(int(row[2]))


# Set flag checked to update record if it's before exist
def SetFindFlag():
    if len(urls) != 0:
        for i in range(0, len(urls)):
            if start_url_maker == urls[i]:
                cur.execute("UPDATE api_urlchecked set hits = '{}' where url = '{}'".format(hits_url[i] + 1, start_url_maker));
                conn.commit()
                return True
    return False


# Insert a new URL if record doesn't exist before
def InsertURL():
    cur.execute("INSERT INTO api_urlchecked (url, hits,broken_links_num) \
                                          VALUES ('{}', '{}' , '{}')".format(start_url_maker, 1, 0));
    conn.commit()


# Print records and results of checking in text file and count broken links
def PrintDataInText():
    brokens_count = 0
    with open(f"links.txt", "w", encoding="utf-8") as f:
        for link in links_array:
            print(link.strip(), file=f)
            url_check = CheckValidation(link)
            if url_check == "URL is invalid":
                x = brokens_count + 1
                brokens_count = x
            print(url_check, file=f)
            print(file=f)
    return brokens_count


# Class of spider for crawling all urls
class Spider(scrapy.Spider):
    # Define name of Spider for starting crawler
    name = "spider"

    # Fetch Broken Links
    FetchBrokenLinks()

    # Set link for crawling
    global allowed_domains
    allowed_domains = [url_input]
    start_urls = [
        start_url_maker
    ]

    # Set URLs of database for check that before used
    FetchUrls()
    find_flag = False
    if SetFindFlag() == True:
        find_flag = True

    # Insert URL if it's not checked before
    if find_flag == False:
        InsertURL()

    # Parsing Function for Run Crawler
    def parse(self, response, **kwargs):
        for link in response.css('a::attr(href)').getall():
            if link != "":
                if link[0] == 'h':
                    if link not in links_array:
                        links_array.append(link)
                        if link.find(allowed_domains[0]) != -1:
                            internal_links.append(link)

        # Depth of crawling, if crawl level is 0, just crawl first page, else check all urls of whole site
        for k in range(0, crawl_level):
            for j in internal_links:
                yield scrapy.Request(url=j, callback=self.parse)

        broken_count = PrintDataInText()

        SetInDatabase(broken_count)

        for i in links_array:
            i = i.replace("http://", "")
            i = i.replace("https://", "")
            if i[len(i) - 1] == "/":
                i = i[:-1]
            i = i.split("/")

            if i[0] not in first_depth:
                first_depth.append(i[0])
                first_depth_tree.append(Node(i[0], parent=root))

            if len(i) > 1:
                for j in range(0, len(first_depth_tree) - 1):
                    if first_depth[j] == i[0] and i[1] not in second_depth:
                        second_depth.append(i[1])
                        second_depth_tree.append(Node(i[1], parent=first_depth_tree[j]))

            if len(i) > 2:
                for j in range(0, len(second_depth_tree) - 1):
                    if second_depth[j] == i[1] and i[2] not in third_depth:
                        third_depth.append(i[2])
                        third_depth_tree.append(Node(i[2], parent=second_depth_tree[j]))

            if len(i) > 3:
                for j in range(0, len(third_depth_tree) - 1):
                    if third_depth[j] == i[2] and i[3] not in fourth_depth:
                        fourth_depth.append(i[3])
                        fourth_depth_tree.append(Node(i[3], parent=third_depth_tree[j]))

            if len(i) > 4:
                for j in range(0, len(fourth_depth_tree) - 1):
                    if fourth_depth[j] == i[3] and i[4] not in fifth_depth:
                        fifth_depth.append(i[4])
                        fifth_depth_tree.append(Node(i[4], parent=fourth_depth_tree[j]))

            if len(i) > 5:
                for j in range(0, len(fifth_depth_tree) - 1):
                    if fifth_depth_tree[j] == i[4] and i[5] not in sixth_depth:
                        sixth_depth.append(i[5])
                        sixth_depth_tree.append(Node(i[5], parent=fifth_depth_tree[j]))

        with open(f"Tree.txt", "w", encoding="utf-8") as f:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))
                print("%s%s" % (pre, node.name), file=f)


def SetInDatabase(broken_links_count):
    start_url_maker_db = "https://" + url_input + "/"
    start_urls_db = [
        start_url_maker_db
    ]
    urls_db = []
    hits_db = []

    cur.execute("SELECT id, url, hits, broken_links_num from api_urlchecked")
    rows = cur.fetchall()
    for row in rows:
        urls_db.append(row[1])
        hits_db.append(int(row[2]))

    if len(urls_db) != 0:
        for i in range(0, len(urls_db)):
            if start_url_maker_db == urls_db[i]:
                print(broken_links_count)
                cur.execute("UPDATE api_urlchecked set hits = '{}', broken_links_num = '{}' where url = '{}'".format(hits_db[i],
                                                                                                           broken_links_count,
                                                                                                           start_urls_db[
                                                                                                               0]));
                conn.commit()
                find_flag = True
