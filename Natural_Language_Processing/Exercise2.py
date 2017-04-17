from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk.data
import numpy as np
import pandas as pd

'''

Part 1: Feature Importances

For the 4 of the 20newsgroups corpus (your choice), find the 10 most
important words by:
    * total tf-idf score
    * average tf-idf score (average only over non-zero values)
    * highest tf (only) score across corpus

'''

#Choose the first four categories
four_categories = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
    'comp.sys.ibm.pc.hardware']

newsgroups = fetch_20newsgroups(subset='train', categories=four_categories)
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(newsgroups.data).toarray()
words = vectorizer.get_feature_names()

#total tf-idf score
total = np.sum(vectors, axis=0)
print "Top 10 by total tf-idf score"
print [words[i] for i in np.argsort(total)[-1:-10-1:-1]]

#average tf-idf score
avg = np.sum(vectors, axis=0) / np.sum(vectors > 0, axis=0)
print "Top 10 by average tf-idf score"
print [words[i] for i in np.argsort(avg)[-1:-10-1:-1]]

#total tf score across corpus
vectorizer2 = TfidfVectorizer(use_idf=False)
vectors2 = vectorizer2.fit_transform([" ".join(newsgroups.data)]).toarray()
print "Top 10 by total tf score"
print [words[i] for i in np.argsort(vectors2[0])[-1:-10-1:-1]]


'''

Part 2: Ranking

Use cosine similarity to rank the relevance of a document to a given search query.
For each query, find the 3 most relevant articles from the 20 Newsgroups corpus.

'''

filenames = newsgroups.filenames
print filenames[0]
with open('data/queries.txt') as f:
    queries = [line.strip() for line in f]

tokenized_queries = vectorizer.transform(queries)
cosine_similarities = linear_kernel(tokenized_queries, vectors)
for i, query in enumerate(queries):
    print query
    print [filenames[i] for i in np.argsort(cosine_similarities[i])[-1:-3-1:-1]]
    print
