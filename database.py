from pymongo import MongoClient

def connectDatabase_pages():
    DB_NAME = "a3"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db.pages
    
    except:
        print("Database not connected succesfully.")

def connectDatabase_professors():
    DB_NAME = "a3"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db.professors
    
    except:
        print("Database not connected succesfully.")
        
def insertProfessor(col, doc):
    col.insert_one(doc)


def insertPage(col, url, title, data):
    document = {
        "URL": url,
        "Title": title,
        "Page Data": data
    }

    col.insert_one(document)

def findPage(col, title):
    pageData = []
    for x in col.find({"Title":title}, {\
        "_id": 0,
        "URL": 1,
        "Title": 1,
        "Page Data": 1
    }):
        pageData.append( x["Page Data"] )
    
    return pageData
    

