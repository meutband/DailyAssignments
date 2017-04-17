Exercise 1 sets up a MongoDB client to access New York Times articles from a json file.
  * Tokenized documents using Snowball Stemmer
  * Count Vectorizer to get counts and feature names
  * TFidf Vectoizer to get counts and feature names
  * Find the 5 most alike documents with cosine similarity

Exercise 2 uses fetch_20 newsgroups from sklearn.datasets.
  * Find 10 most important words in 4 corpuses using tfidf score and tf score
  * Rank the 3 most relavent articles from the corpuses using cosine similarity
