#! bin/var/env

import pandas as pd
import praw


def text_usrnm_gatherer(subreddit_source, flag, content='comments', n=100):
    # Connecting to reddit, loading the right subreddit
    conn = praw.Reddit('PTSD parser 1.o')
    subreddit = conn.get_subreddit(subreddit_source)

    # Initializing objects to be populated
    usernames = []
    stories = pd.DataFrame()

    # Getting usernames from subreddit
    for submission in subreddit.get_top_from_all(limit=n):
        usernames.append(submission.author)

    # Loading posts from the usernames, whether comments or posts
    if content == 'comments':
        for user in usernames:

            for post in user.get_comments(limit=n):

                temp_dict = {'text': post, 'flag': flag, 'user': user}
                temp_df = pd.DataFrame(temp_dict, index=[user])
                stories = pd.concat([stories, temp_df])

    elif content == 'posts':
        for user in usernames:
            for post in user.get_submitted(limit=n):

                temp_dict = {'text': post.selftext, 'flag': flag, 'user': user}
                temp_df = pd.DataFrame(temp_dict, index=[user])
                stories = pd.concat([stories, temp_df])

    return stories


def main():

    ptsd_stories = text_usrnm_gatherer('ptsd', 'PTSD', content='comments', n=1000)
    non_ptsd_stories = text_usrnm_gatherer('tifu', 'non_PTSD', content='comments', n=1000)
    output = pd.concat([ptsd_stories, non_ptsd_stories])
    output.to_pickle('reddit_data.p')

    return output


if __name__ == '__main__':
    main()
