#! bin/var/env

import pandas as pd
import praw


def text_sub_gatherer(subreddit_name, flag, n=100):
    conn = praw.Reddit('PTSD parser 1.o')

    subreddit = conn.get_subreddit(subreddit_name)

    stories = pd.DataFrame()

    for submission in subreddit.get_hot(limit=n):
        temp_dict = {'text': submission.selftext, 'flag': flag}
        temp_df = pd.DataFrame(temp_dict, index=[submission.id])
        stories = pd.concat([stories, temp_df])

    return stories


def main():
    stories = text_sub_gatherer('ptsd', 'PTSD')
    print stories.head()
    return stories

if __name__ == '__main__':
    main()
