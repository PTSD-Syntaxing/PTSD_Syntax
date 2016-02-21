#! bin/var/env

from bs4 import BeautifulSoup
import pandas as pd
import re
import reddit_scrapper
import xgboost as xgb

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import cross_val_score


def post_cleaner(story):

    text = BeautifulSoup(story).get_text()
    letters_only = re.sub('[^a-zA-Z]', ' ', text)
    lower_case = letters_only.lower()
    words = lower_case.split()

    stops = set(stopwords.words('english') + ['ptsd'])

    meaningful_words = [w for w in words if not w in stops]

    output = ' '.join(meaningful_words)

    return output


def model_creation(df):
    # Cleaning the target variable, removing poorly encoded rows and turning into binary
    df['flag'].replace(to_replace='PTSD', value=1, inplace=True)
    df['flag'].replace(to_replace='non_PTSD', value=0, inplace=True)
    df = df[df['flag'].isin([0, 1])]

    target = df['flag'].copy()
    print target.value_counts()

    # Cleaning the posts to remove markup and vectorizing
    df['text'] = df['text'].astype(str).apply(post_cleaner)

    vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    preds = vectorizer.fit_transform(df['text'])
    preds = pd.DataFrame(preds.todense(), index=df.index)

    # Putting values into DMatrix for performance reasons, initializing xgboost params and training model
    xgtrain = xgb.DMatrix(preds.values, target.values)

    xgboost_params = {'objective': 'binary:logistic', 'booster': 'gbtree', 'eval_metric': 'auc', 'eta': 0.01,
                      'subsample': 0.75, 'colsample_bytree': 0.68, 'max_depth': 7}

    results = xgb.cv(xgboost_params, xgtrain, num_boost_round=5, nfold=5, metrics={'error'}, seed=0, show_stdv=False)

    # luke messing up sebastian's pristine code
    y = target.astype(int).values
    X = preds.values

    rf = RandomForestClassifier()
    nb = BernoulliNB()

    cv1 = cross_val_score(rf, X, y)
    cv2 = cross_val_score(nb, X, y)

    print results['test-error-mean'].mean(), sum(cv1) / len(cv1), sum(cv2) / len(cv1)


def main():
    # data = reddit_scrapper.main()
    data2 = pd.read_csv('reddit__usrnm_data.csv', index_col=0)
    model_creation(data2)


if __name__ == '__main__':
    main()
