#! bin/var/env

import pandas as pd
import praw


def text_sub_gatherer(subreddit_name, flag, n=100):
    conn = praw.Reddit('PTSD parser 1.o')

    subreddit = conn.get_subreddit(subreddit_name)

    stories = pd.DataFrame()

    for submission in subreddit.get_top_from_all(limit=n):

        temp_dict = {'text': submission.selftext, 'flag': flag}
        temp_df = pd.DataFrame(temp_dict, index=[submission.id])
        stories = pd.concat([stories, temp_df])

    return stories


def main():

    ptsd_stories = text_sub_gatherer('ptsd', 'PTSD', n=1000)
    non_ptsd_stories = text_sub_gatherer('tifu', 'non_PTSD', n=1000)
    output = pd.concat([ptsd_stories, non_ptsd_stories])
    output.to_pickle('reddit_data.p')
    
    return output


if __name__ == '__main__':
    main()
