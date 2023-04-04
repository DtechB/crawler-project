import os
import sys

print(sys.argv)

def getSubdomains(url):
    os.system("python C:/Users/MosKn/Desktop/crawler-project/modulds/findSubDomains/findSubDomains.py" +
              " " + url)
    
def getSsl(url):
    os.system("python C:/Users/MosKn/Desktop/crawler-project/modulds/ssl-checker/ssl_checker.py" +
              " -H " + url)
    

    

url = sys.argv[1]
getSubdomains(url)
getSsl(url)
#getCrawler("shahroodut.ac.ir")