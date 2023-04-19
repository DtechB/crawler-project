import os
import sys
import requests


def sendStartOper(operation):
    dicordUrl = 'https://discord.com/api/webhooks/1097415706749976668/dIl7KBPNmwIyN_WF8bFH9imhsPSW41ZxcWE1JvoZbPYl6H4lQU4RLFtlYxaL9ay7lJPN'
    message = {'content': operation + ' of ' + url + ' is running...'}
    x = requests.post(dicordUrl, json=message)


def sendFinishOper(operation):
    dicordUrl = 'https://discord.com/api/webhooks/1097415706749976668/dIl7KBPNmwIyN_WF8bFH9imhsPSW41ZxcWE1JvoZbPYl6H4lQU4RLFtlYxaL9ay7lJPN'
    message = {'content': operation + ' of ' + url + ' is Completed'}
    x = requests.post(dicordUrl, json=message)


def getSubdomains(url):
    sendStartOper("Subdomain")
    os.system("python C:/Users/MosKn/Desktop/crawler-project/modulds/findSubDomains/findSubDomains.py" +
              " " + url)
    sendFinishOper("Subdomain")


def getSsl(url):
    sendStartOper("SSL")
    os.system("python C:/Users/MosKn/Desktop/crawler-project/modulds/ssl-checker/ssl_checker.py" +
              " -H " + url)
    sendFinishOper("SSL")


url = sys.argv[1]
getSubdomains(url)
getSsl(url)
# getCrawler("shahroodut.ac.ir")
