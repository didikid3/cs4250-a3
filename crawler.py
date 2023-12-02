from urllib.request import urlopen
from bs4 import BeautifulSoup
import time 
from pymongo import MongoClient
import database

class Link:
    def __init__(self, url):
        self.url = url

links = [Link('https://www.cpp.edu/sci/computer-science/index.shtml')]
visited = []
permanentFacultyPage = None

db = database.connectDatabase_pages()

def merge(start, relPath):
    return "https://www.cpp.edu" + relPath

def checkDuplicate(q, element):
    for item in q:
        if element == item.url:
            return True
    return False

def isPermanentFaculty(bs):
    for data in bs.find_all('title'):
        title = data.get_text().strip().replace('\n',"")
        return (title, "Permanent Faculty" == title)
        
def extractLinks(bs, q, currentSite):
    body = bs.find('body')
    for div in body.find_all('div'):
        for data in div.find_all('a', {'class':'nav-link'}):
            link = data.get('href')
            
            if "https" in link:
                if not checkDuplicate(q, link):
                    q.append(Link(link))             
            elif link[0] == "/":
                new = merge(currentSite.url, link)
                if not checkDuplicate(q, new):
                    q.append(Link(new))
            else:
                pass

def crawler(links, visited):
    while links:
        nextURL = links.pop(0)
        if nextURL.url in visited:
            continue
        visited.append(nextURL.url)
        print("Queue Size:", str(len(links)))
        print("Visiting " + nextURL.url)

        html = urlopen(nextURL.url)
        data = html.read()
        

        bs = BeautifulSoup(data, 'html.parser')

        #Move on to Parser if Found Faculty Page
        title, correctPage = isPermanentFaculty(bs)

        database.insertPage(db, nextURL.url, title, data)
        if correctPage:
            permanentFacultyPage = nextURL
            print("Found Permanent Faculty")
            print("Time Taken:", str(time.time() - startTime))
            break

        extractLinks(bs, links, nextURL)

startTime = time.time()
# Crawler
# crawler(links, visited)

#Parser
pages = database.findPage(db, "Permanent Faculty")
data = None
for page in pages:
    data = page.decode()

def parser(data):
    bs = BeautifulSoup(data, "html.parser")
    prof_db = database.connectDatabase_professors()
    for div in bs.find('main').find_all('div', {'id':'main'}):
        for prof in div.find_all('div', {'class': 'clearfix'}):
            name = prof.find('h2')
            if name is not None:
                document = {}
                document['Name'] = name.get_text().strip()

                prof_info = prof.find('p')
                for info in prof_info.find_all('strong'):
                    if 'Email' in info.get_text() or 'Web' in info.get_text():
                        document[info.get_text().replace(":","").strip()] = info.find_next_sibling(href=True)['href'].replace("mailto:","")
                    else:
                        document[info.get_text().replace(":","").strip()] = info.find_next_sibling(string=True).replace(':',"").strip()
                        
                print(document)
                database.insertProfessor(prof_db, document)
                print("---")

parser(data)