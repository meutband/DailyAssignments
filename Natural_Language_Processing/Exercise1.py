from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

'''
Setup using MongoDB.

- Marks-MBP:nlp meutband$ sudo mongod

#Without closing, open a new terminal tab

- Marks-MacBook-Pro:nlp meutband$ mongoimport --db nyt_dump --collection articles
data/articles_mongoimport.json --batchSize 1

Now from python:
'''

'''
1. load all of the article content from the collection into a list of strings
where each individual string is a NY Times article.
'''

client = MongoClient()
db = client.nyt_dump
coll = db.articles
documents = ['\n'.join(article['content']) for article in coll.find()]

'''
2. Write a function that will tokenize the documents and use SnowballStemmer to
stemitize the documents.
'''

snowball = SnowballStemmer('english')

def tokenize(doc):
    return [snowball.stem(word) for word in word_tokenize(doc.lower())]


'''
3. Apply CountVectorizer. Print the counts and then print the feature names
'''

countvect = CountVectorizer(stop_words='english', tokenizer=tokenize)
count_vectorized = countvect.fit_transform(documents)
print count_vectorized

words = countvect.get_feature_names()
print words

'''
4. Apply TfidfVectorizer. Print the vectors and then print the feature names
'''

tfidfvect = TfidfVectorizer(stop_words='english', tokenizer=tokenize)
tfidf_vectorized = tfidfvect.fit_transform(documents)
print tfidf_vectorized

words_tfidf = tfidfvect.get_feature_names()
print words_tfidf

'''
5. Find the cosine similarity between 2 documents. Find the 5 most alike document pairs
'''

# TfidfVectorizer can produce normalized vectors, in which case cosine_similarity
# is equivalent to linear_kernel, only slower.

cosine_similarities = linear_kernel(tfidf_vectorized, tfidf_vectorized)

results = pd.DataFrame()

d1 = []
d2 = []
cs = []

for i, doc1 in enumerate(documents):
    for j, doc2 in enumerate(documents):
        if i != j:
            d1.append(i)
            d2.append(j)
            cs.append(cosine_similarities[i,j])


results['Document1'] = d1
results['Document2'] = d2
results['Cosine Similarity'] = cs

results.sort_values(by='Cosine Similarity', ascending='False')

print results.head(5)
