import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer

# from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == '__main__':
    # Load data
    with open('raw_text/blogs/PTSD/jeff_ptsd.txt', 'r') as f:
        read_data = f.read()
    word_bag = read_data.split()


    # lowercase & lemmatize
    word_bag = [word.lower().decode('utf-8') for word in word_bag]

    wnl = WordNetLemmatizer()
    X = [wnl.lemmatize(word) for word in word_bag]

    # Vectorize
    cntr = CountVectorizer(input='content', strip_accents='ascii', ngram_range=(1, 1), stop_words='english')
    out = cntr.fit_transform(X)
