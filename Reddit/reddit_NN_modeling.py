#!bin/var/env python 2.7

import h2o
import pandas as pd
import re
import csv

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def post_cleaner(story):

    # Removing HTML markup using beautiful soup, removing non letter chars and lowercasing everything
    text = BeautifulSoup(story, 'lxml').get_text()
    letters_only = re.sub('[^a-zA-Z]', ' ', text)
    lower_case = letters_only.lower()

    # Making strings a list of strings for faster performance
    words = lower_case.split()

    # Putting stopwords in a set for faster performance, adding the word PTSD
    stops = set(stopwords.words('english') + ['ptsd'])

    # Removing stop words
    meaningful_words = [w for w in words if not w in stops]

    # Rejoining string
    output = ' '.join(meaningful_words)

    return output


def neural_network(df):
    h2o.init()
    # Cleaning the target variable, removing poorly encoded rows and turning into binary
    df['flag'].replace(to_replace='PTSD', value=1, inplace=True)
    df['flag'].replace(to_replace='non_PTSD', value=0, inplace=True)
    df = df[df['flag'].isin([0, 1])]

    target = df['flag'].copy()

    # Cleaning the posts to remove markup and vectorizing
    df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore'))
    df['text'] = df['text'].apply(post_cleaner)

    vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    preds = vectorizer.fit_transform(df['text'])
    preds = pd.DataFrame(preds.todense(), index=df.index)

    preds.to_csv('preds.csv', quoting=csv.QUOTE_ALL)
    h2o_preds = h2o.import_file('preds.csv')
    print h2o_preds

def main():
    data = pd.read_pickle('reddit_data.p')
    model_output = neural_network(data)


if __name__ == '__main__':
    main()
