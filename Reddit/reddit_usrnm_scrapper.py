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
    # Broad exception acknowledged, should be changed in future
    if content == 'comments':
        for user in usernames:
            try:
                for post in user.get_comments(limit=n):

                    temp_dict = {'text': post, 'flag': flag, 'user': user}
                    temp_df = pd.DataFrame(temp_dict, index=[user])
                    stories = pd.concat([stories, temp_df])
            except:
                print 'This user has no comments. :('

    elif content == 'posts':
        for user in usernames:
            try:
                for post in user.get_submitted(limit=n):

                    temp_dict = {'text': post.selftext, 'flag': flag, 'user': user}
                    temp_df = pd.DataFrame(temp_dict, index=[user])
                    stories = pd.concat([stories, temp_df])
            except:
                print 'This user has no posts. :('

    return stories


def main():

    ptsd_stories = text_usrnm_gatherer('ptsd', 'PTSD', content='posts', n=100)
    non_ptsd_stories = text_usrnm_gatherer('tifu', 'non_PTSD', content='posts', n=100)
    output = pd.concat([ptsd_stories, non_ptsd_stories])
    output.to_csv('reddit__usrnm_data.csv', index=False)

    return output


if __name__ == '__main__':
    main()
