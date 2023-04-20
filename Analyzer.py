import psycopg2
import os
import sys
from decouple import config

from modulds.ssl_checker import ssl_checker
from modulds.findSubDomains import findSubDomains


# def runAnalyzer(url):
#     os.system("python C:/Users/MosKn/Desktop/crawler-project/Analyze.py" + " " + url)

# Connect to database
conn = psycopg2.connect(database="Alpha", user=config('DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="localhost", port="5432")
cur = conn.cursor()

# Create an array for conainter of pending urls
pendingList = []

# Get List of pending from the database and added them into array
def FetchPendingLinks():
    cur.execute("SELECT id, url, status from api_site")
    rows = cur.fetchall()
    for row in rows:
        pendingElement = {}
        pendingElement.update({"id": row[0]})
        pendingElement.update({"url": row[1]})
        pendingElement.update({"status": row[2]})
        pendingList.append(pendingElement)
    return pendingList


# Update List of pending urls to proccessed urls the database and added them into array
def UpdateUrlCondition(url):
    cur.execute("UPDATE api_site set status = '{}' where url = '{}'".format("A", url));
    conn.commit()
    return True
        

# For loop for getting pending and run SSL, Subdomain and Crawler
def analyze():
    data = FetchPendingLinks()
    for i in data:
        if i['status'] == "P":
            ssl_checker.run( i['id'],i['url'])
            UpdateUrlCondition(i['url'])
