import psycopg2
from decouple import config
import requests
import os

# from modulds.ssl_checker import ssl_checker
# from modulds.findSubDomains import findSubDomains

# Connect to database
conn = psycopg2.connect(database="alpha", user=config(
    'DATABASE_USERNAME'), password=config('DATABASE_PASSWORD'), host="localhost", port="5432")
cur = conn.cursor()

# Send message to discord bot for start running link (Log information)


def sendStartOper(operation, url):
    dicordUrl = 'https://discord.com/api/webhooks/1097415706749976668/dIl7KBPNmwIyN_WF8bFH9imhsPSW41ZxcWE1JvoZbPYl6H4lQU4RLFtlYxaL9ay7lJPN'
    message = {'content': operation + ' of ' + url + ' is running...'}
    x = requests.post(dicordUrl, json=message)


# Send message to discord bot for finsih running link (Log information)
def sendFinishOper(operation, url):
    dicordUrl = 'https://discord.com/api/webhooks/1097415706749976668/dIl7KBPNmwIyN_WF8bFH9imhsPSW41ZxcWE1JvoZbPYl6H4lQU4RLFtlYxaL9ay7lJPN'
    message = {'content': operation + ' of ' + url + ' is Completed'}
    x = requests.post(dicordUrl, json=message)


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
    cur.execute(
        "UPDATE api_site set status = '{}' where url = '{}'".format("A", url))
    conn.commit()
    return True


# For loop for getting pending and run SSL, Subdomain and Crawler
def analyze():
    data = FetchPendingLinks()
    for i in data:
        if i['status'] == "P":

            # sendStartOper("SSL", i['url'])
            # ssl_checker.runSSLChecker(i['id'], i['url'])
            # sendFinishOper("SSL", i['url'])

            # sendStartOper("Subdomain", i['url'])
            # findSubDomains.runSubdomain(i['id'], i['url'])
            # sendFinishOper("Subdomain", i['url'])
            
            # sendStartOper("Crawler", i['url'])
            # os.system('cmd /k "dir"')
            # sendFinishOper("Crawler", i['url'])

            UpdateUrlCondition(i['url'])
