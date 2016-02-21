#! bin/var/env

from bs4 import BeautifulSoup
import pandas as pd
import re
import reddit_scrapper
import xgboost as xgb

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

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

    df['text'] = df['text'].apply(post_cleaner)

    vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    preds = vectorizer.fit_transform(df['text'])
    preds = pd.DataFrame(preds.todense(), index=df.index)

    labels = LabelEncoder().fit(df['flag'])
    target = pd.Series(labels.transform(df['flag']), index=df.index)

    xgtrain = xgb.DMatrix(preds.values, target.values)

    xgboost_params = {'objective': 'binary:logistic', 'booster': 'gbtree', 'eval_metric': 'auc', 'eta': 0.01,
                      'subsample': 0.75, 'colsample_bytree': 0.68, 'max_depth': 7}

    results = xgb.cv(xgboost_params, xgtrain, num_boost_round=5, nfold=5, metrics={'error'}, seed=0, show_stdv=False)

    # luke messing up sebastian's pristine code
    y = target.values
    X = preds.values

    rf = RandomForestClassifier()
    nb = BernoulliNB()

    cv1 = cross_val_score(rf, X, y)
    cv2 = cross_val_score(nb, X, y)

    print results['test-error-mean'].mean(), sum(cv1) / len(cv1), sum(cv2) / len(cv1)


def main():
    data = reddit_scrapper.main()
    model_creation(data)


if __name__ == '__main__':
    main()
