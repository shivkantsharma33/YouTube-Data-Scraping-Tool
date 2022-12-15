import requests
import os
import pandas as pnd
import time as t

tx = t.localtime()
timestamp = t.strftime('%b-%d-%Y_%H%M', tx)


url_3="https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&key=AIzaSyCakWxeGn02IndtoyJDiEXL70B8Mqfq6K0&id="
url_1 = "https://www.googleapis.com/youtube/v3/channels?part=id&key=AIzaSyCakWxeGn02IndtoyJDiEXL70B8Mqfq6K0&id="
url_2 = "https://www.googleapis.com/youtube/v3/channels?part=statistics&key=AIzaSyCakWxeGn02IndtoyJDiEXL70B8Mqfq6K0&id="
url_comments="https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&key=AIzaSyCakWxeGn02IndtoyJDiEXL70B8Mqfq6K0&videoId="

temp = ""
videoid_list = list()
commentid_list = list()
# like_count_list=list()
# view_count_list=list()
# dislike_count_list=list()
# comment_count_list=list()
time_count_list = list()
comment_text_list = list()
description = list()
# duration=list()
author_list = list()


# a52, a72 , review_comparison, tt , review

# def read_YT_pagelist():
#     print("Reading XL work book")
#     df = pnd.read_excel(open(r'C:\Users\shivkant.s\Desktop\YT_Comment_ID.xlsx', 'rb'), sheet_name='Sheet2')
#     page_list = pnd.Series.dropna(df['Video_ID'])
#
#     return page_list


def user_Type(name, type):
    if type == "channel":
        temp = url_2 + name;
        print(temp)

    if type == "user":
        temp = url_1 + name;
        print(temp)

    return temp


# def write_Xlbook(df):
#     tx = t.localtime()
#     timestamp = t.strftime('%b-%d-%Y_%H%M ', tx)
#     writer = pnd.ExcelWriter('vidoe yt social comments- output on ' + timestamp + '.xlsx')
#     # writer = pnd.ExcelWriter('output.xlsx')
#     df.to_excel(writer, 'Sheet1', index=False)
#     writer.save()
#     return


from tqdm import tqdm


def get_YT_subcount(page_name):
    count = 0
    df_final = pnd.DataFrame()
    for page in tqdm(page_name):
        i = 1
        # print(url_1,page)
        # data1=requests.get((url_1+page)).json()
        # if data1['totalResults']==0 :
        #    continue
        # videoid_list.append(page)

        data = requests.get((url_comments + page)).json()
        next_page_token = ''
        # print(page)
        while i:
            try:
                data = requests.get((url_comments + page + "&pageToken=" + next_page_token)).json()
                next_page_token = data['nextPageToken']
            except Exception as kex:
                print('Excption is e', kex)
                i = 0
            try:

                for item in data['items']:
                    if 'replies' in item:
                        # print("in replies part")
                        # print(item['replies']['comments'][0].keys())
                        for reply_item in item['replies']['comments']:
                            count += 1
                            # print(reply_item['snippet'].keys())
                            videoid_list.append(page)
                            time_count_list.append(reply_item['snippet']['publishedAt'])
                            comment_text_list.append(reply_item['snippet']['textOriginal'])
                            author_list.append(reply_item['snippet']['authorDisplayName'])
                            # print('idis ',reply_item['id'])
                            commentid_list.append(reply_item['id'])
                            # print("Counter is ",count)

                    count += 1

                    videoid_list.append(page)
                    time_count_list.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    comment_text_list.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
                    author_list.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    commentid_list.append(item['snippet']['topLevelComment']['id'])
                    # duration=list()
            except KeyError as keyex:
                if 'items' in str(keyex):
                    break
            # print(url_comments+page+"&pageToken="+next_page_token)

            # print("Data is",data)

    df_final = df_final.assign(Comment_ID=commentid_list).assign(Author_Name=author_list).assign(
        Text=comment_text_list).assign(Time_stamp=time_count_list).assign(Video_id=videoid_list)

    df_final.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/YT Comments ' + timestamp + '.xlsx',index=False)

    return df_final




