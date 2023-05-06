import os

def runCrawler(id, link):
    os.system('scrapy crawl spider ' + link)
