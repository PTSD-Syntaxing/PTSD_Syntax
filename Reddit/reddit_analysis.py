#! bin/var/env

from bs4 import BeautifulSoup
import pandas as pd
import re
import reddit_scrapper
import xgboost as xgb

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder


def post_cleaner(story):

    text = BeautifulSoup(story).get_text()
    letters_only = re.sub('[^a-zA-Z]', ' ', text)
    lower_case = letters_only.lower()
    words = lower_case.split()

    stops = set(stopwords.words('english'))

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

    return results



def main():
    data = reddit_scrapper.main()
    scores = model_creation(data)
    print scores
    return scores

if __name__ == '__main__':
    scores_sorry_sebastian = main()
