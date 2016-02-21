#! bin/var/env

from bs4 import BeautifulSoup
import pandas as pd
import re
import reddit_scrapper

from nltk.corpus import stopwords


def post_cleaner(story):

    text = BeautifulSoup(story).get_text()
    letters_only = re.sub('[^a-zA-Z]', ' ', text)
    lower_case = letters_only.lower()
    words = lower_case.split()


def main():
    stories = reddit_scrapper.main()
    print reviews.head()
