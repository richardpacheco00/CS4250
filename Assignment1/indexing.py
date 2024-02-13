#-------------------------------------------------------------------------
# AUTHOR: Richard Pacheco
# FILENAME: indexing.py
# SPECIFICATION: analyzes an input file 'collection.csv' and creates a tf-idf table for the words after pruning it of extraneous terms
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hours (for the coding segment)
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal. Hint: use a set to define your stopwords.

stopwords = {'I', 'and', 'She', 'her', 'They', 'their'}
stopwordsRemoved = []
for document in documents:
  words = document.split()
  noStopwords = ""
  for word in words:
    if word not in stopwords:
      noStopwords += word + " "
  stopwordsRemoved.append(noStopwords.strip())

  

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.

stemming = {"cats":"cat", 
            "loves":"love", 
            "dogs":"dog"}
wordsStemmed = []
for document in stopwordsRemoved:
  words = document.split()
  stemmed = ""
  for word in words:
    if word in stemming:
      stemmed += stemming[word] + " "
    else:
      stemmed += word + " "
  wordsStemmed.append(stemmed.strip())
  


#Identifying the index terms.

# convert wordsStemmed array into a dictionary with document IDs and the strings split into words
documentsWithIDs = dict()
index = 1
for document in wordsStemmed:
  documentsWithIDs[index] = document.split()
  index += 1
  
# iterate through the documents
terms = {}
for id in documentsWithIDs:
  for word in documentsWithIDs[id]:
    if word not in terms:
      terms[word] = {id}
    else:
      terms[word].add(id)
      
  


#Building the document-term matrix by using the tf-idf weights.

# calculate Document Frequency for each term
documentFrequency = dict()
for term in terms:
  documentFrequency[term] = len(terms[term])

print(documentFrequency)
# count total documents
numDocuments = len(documentsWithIDs)

# create the tf-idf matrix
tfidfMatrix = {}

# fill the matrix
for term in terms:
  
  #calculate inverse document frequency
  if(documentFrequency[term] == 0):
    idf = 0
  else:
    idf = math.log(numDocuments / (documentFrequency[term]))
  
  # compute tf-idf for each document with the term in it
  for documentID in terms[term]:
    currentDocument = documentsWithIDs[documentID]
    
    # calculate term frequency and tfidf
    tf = currentDocument.count(term) / len(currentDocument)
    
    tfidf = tf*idf
    
    # store tf-idf in the tf-idf matrix
    if term not in tfidfMatrix:
      # if not already in the matrix, initialize a new dict with the {document: tfidf} pair respectively
      tfidfMatrix[term] = {documentID: tfidf} 
    else:
      tfidfMatrix[term][documentID] = tfidf
  

#Printing the document-term matrix.
for term, scores in tfidfMatrix.items():
  print(f"Term: {term}")
  for documentID, tfidfScore in scores.items():
    print(f"  Document {documentID}: {tfidfScore}")
    
