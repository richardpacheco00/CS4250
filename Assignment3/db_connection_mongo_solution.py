#-------------------------------------------------------------------------
# AUTHOR: Richard Pacheco
# FILENAME: db_connection_mongo_solution.py
# SPECIFICATION: Defines a set of functions to connect to a MongoDB database and create, delete, and edit documents.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
from collections import Counter 
import string

host = 'localhost'
PORT = 27017

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient(host, PORT)
    client.admin.command('ping')
    print("Connected")
    db = client.database_name
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary indexed by term to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    dict = Counter(docText.translate(str.maketrans('', '', string.punctuation)).lower().split(" "))

    # create a list of objects to include full term objects. [{"term", count, num_char}]
    # --> add your Python code here
    objs = [[term, count, len(term)] for term, count in dict.items() if term != ""]

    # produce a final document as a dictionary including all the required document fields
    # --> add your Python code here
    doc = {
        "doc": docId,
        "Text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "num_chars": sum([obj[1] * obj[2] for obj in objs]),
    }

    # insert the document
    # --> add your Python code here
    col.insert_one(doc)
    return 

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    col.delete_one( { "doc": docId } )
    return 

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    res = col.delete_one( { "doc": docId } ) # fix
    if not res.acknowledged:
        print("No document with this id to update ")
        return

    # Create the document with the same id
    # --> add your Python code here
    createDocument(col, docId, docText, docTitle, docDate, docCat)
    return 

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    idx = {}
    for doc in col.find():
        title = f"{doc['title']}:{doc['doc']}"
        words = Counter(doc['Text'].translate(str.maketrans('', '', string.punctuation)).lower().split(" "))
        for w in words: 
            if w == "":
                pass
            else: 
                
                if w not in idx: 
                    idx[w] = title
                else: 
                    idx[w] = idx[w] + f',{title}'

    return str(idx) 