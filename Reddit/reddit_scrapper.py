#! bin/var/env

import praw
import pandas as pd

r = praw.Reddit('PTSD parser 1.o')


def text_sub_gatherer(id_list, flag):
    stories = pd.DataFrame()

    for i, id_val in enumerate(id_list):

        print id_val
        submission = r.get_submission(submission_id=id_val)
        temp_dict = {'id_thread': id_val, 'text': submission, 'flag': flag}
        temp_df = pd.DataFrame(temp_dict, index=[i])
        stories = pd.concat([stories, temp_df])

    return stories


def ptsd_data_gatherer(ptsd_list, non_ptsd_list):

    ptsd_stories = text_sub_gatherer(ptsd_list, 'PTSD')
    non_ptsd_stories = text_sub_gatherer(non_ptsd_list, 'not PTSD')

    output = pd.concat([ptsd_stories, non_ptsd_stories])

    return output


def main():
    ptsd_list = ['3p0bqz', '3ksgtk', '3fyjhl', '3mp7hy', '3mxwx4', '3jyea5', '3troe9', '2ozj1z', '2n238f', '2zkaak',
                 '20kjwz', '23u2ia', 'sl8gt', '16we1y', '1hog4f', '1nmskv', '16nkjh', '1va3is']
    non_ptsd_list = ['46ph7l', '46jqd5', '46f1p4', '46h5gh', '46cegj']

    stories = ptsd_data_gatherer(ptsd_list, non_ptsd_list)
    return stories

if __name__ == '__main__':
    main()
