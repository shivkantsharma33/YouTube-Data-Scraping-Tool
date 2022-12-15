from googleapiclient.discovery import build
import pandas as pd
# import seaborn as sns
import numpy as np
import time as t
import warnings
warnings.filterwarnings('ignore')

tx = t.localtime()
timestamp = t.strftime('%b-%d-%Y_%H%M', tx)
def scrap(df,limit):
    channel_ids=df['Channel id']

    api_key = 'AIzaSyCakWxeGn02IndtoyJDiEXL70B8Mqfq6K0'

    youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_stats(youtube, channel_ids):
        all_data = []
        for i in range(0, len(channel_ids), 50):
            request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids[i:i + 50]))
            response = request.execute()

            for i in range(len(response['items'])):
                data = dict(Channel_name=response['items'][i]['snippet']['title'],
                            Subscribers=response['items'][i]['statistics']['subscriberCount'],
                            Views=response['items'][i]['statistics']['viewCount'],
                            Total_videos=response['items'][i]['statistics']['videoCount'],
                            playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
                all_data.append(data)

        return all_data

    channel_statistics = get_channel_stats(youtube, channel_ids)

    channel_data = pd.DataFrame(channel_statistics)

    # channel_data

    channel_data.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/Channel_Details.xlsx',index=False)

    def get_video_ids(youtube, playlist_id):

        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=limit)
        response = request.execute()

        video_ids = []
        channel_id = []

        print(len(response['items']))

        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
            channel_id.append(playlist_id)

        next_page_token = response.get('nextPageToken')

        return video_ids, channel_id

    video_ids = []
    channel_ids = []
    for i in range(0, len(channel_data['Channel_name'])):
        playlist_id = channel_data['playlist_id'][i]
        print(playlist_id)

        vdo_id, channel_id = get_video_ids(youtube, playlist_id)

        video_ids.extend(vdo_id)
        channel_ids.extend(channel_id)

    len(video_ids)

    Title = []
    Published_date = []
    Views = []
    Likes = []
    Description = []
    vdo_id = []
    Channel_id = []
    Comments = []
    Channel_name = []
    Video_Url = []

    # df_final = pd.DataFrame()

    def get_video_details(youtube, video_ids):
        # all_video_stats = []
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids[i:i + 50]))
            response = request.execute()

            for video in response['items']:
                try:
                    Title.append(video['snippet']['title'])
                except:
                    Title.append("")

                try:
                    Published_date.append(video['snippet']['publishedAt'])
                except:
                    Published_date.append('')

                try:
                    Views.append(video['statistics']['viewCount'])
                except:
                    Views.append(0)

                try:
                    Likes.append(video['statistics']['likeCount'])
                except:
                    Likes.append(0)

                try:
                    Description.append(video['snippet']['description'])
                except:
                    Description.append("")

                try:
                    vdo_id.append(video['id'])
                except:
                    vdo_id.append('')

                try:
                    Channel_id.append(video['snippet']['channelId'])
                except:
                    Channel_id.append(' ')

                try:
                    Comments.append(video['statistics']['commentCount'])
                except:
                    Comments.append(0)

                try:
                    Channel_name.append(video['snippet']['channelTitle'])
                except:
                    Channel_name.append("")

                try:
                    Video_Url.append("https://www.youtube.com/watch?v=" + video['id'])
                except:
                    Video_Url.append("")

        #     video_stats = dict(Title=Title,Published_date=Published_date,Views=Views,Likes=Likes,Comments=Comments,Description=Description,vdo_id=vdo_id,Channel_id=Channel_id,Channel_name=Channel_name)
        #     all_video_stats.append(video_stats)

        df_final = pd.DataFrame(
            {'Title': Title,
             'Published_date': Published_date,
             'Views': Views,
             'Likes': Likes,
             'Comments': Comments,
             'Description': Description,
             'video_id': vdo_id,
             'Channel_id': Channel_id,
             'Channel_name': Channel_name,
             'Video_Url': Video_Url
             })

        return df_final

    video_details = get_video_details(youtube, video_ids)

    video_data = pd.DataFrame(video_details)

    video_data = video_data.apply(pd.to_numeric, errors='ignore')

    # video_data

    matches = ['UCBJycsmduvYEL83R_U4JriQ',
               'UC9fSZHEh6XsRpX-xJc6lT3A',
               'UCXuqSBlHAE6Xw-yeJA0Tunw',
               'UCsTcErHg8oDvUnTzoqsYeNw',
               'UCXGgrKt94gR6lmN4aN3mYTg',
               'UCDlQwv99CovKafGvxyaiNDA',
               'UCR0AnNR7sViH3TWMJl5jyxw',
               'UCMiJRAwDNSNzuYeN2uWa0pA',
               'UCey_c7U86mJGz1VJWH5CYPA',
               'UCB2527zGV3A0Km_quJiUaeQ']
    video_data['Type'] = ''
    for i in range(0, len(video_data['Channel_id'])):
        a_string = video_data['Channel_id'][i]
        # print(a_string)
        if any(x in a_string for x in matches):
            video_data['Type'][i] = "Global"
        else:
            video_data['Type'][i] = "Local"

    video_data.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/YT_Engagement_Overall_'+timestamp+'.xlsx',index=False)

    return video_data

def datefilter(video_data,s_date,e_date):
    video_data["IST"] = ''
    video_data["IST"] = video_data["Published_date"].str.replace(r'T', ' ')
    video_data["IST"] = video_data["IST"].str.replace(r'Z', '')

    video_data["IST"] = pd.to_datetime(video_data["IST"], format="%Y/%m/%d %H:%M:%S")
    output = (video_data.set_index("IST")
              .tz_localize("utc")
              .tz_convert("Asia/Kolkata")
              .reset_index()
              )
    output['IST'] = output['IST'].dt.tz_localize(None)
    output.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/IST data.xlsx',index=False)
    n_df=output

    s_date = pd.to_datetime(s_date)
    e_date = pd.to_datetime(e_date)
    print(s_date)
    print(e_date)

    nn_df = n_df[(n_df['IST'] >= s_date) & (n_df['IST'] <= e_date)]

    nnn_df=nn_df

    nn_df["Title"] = nn_df["Title"].str.lower()
    nn_df["Description"] = nn_df["Description"].str.lower()

    # nn_df = n_df[(pd.to_datetime(n_df['IST']) >= s_date) & (pd.to_datetime(n_df['IST']) <= e_date)]
    # s_df = nn_df[nn_df["Title"].str.contains("Samsung") | nn_df["Title"].str.contains("Galaxy")]

    def expired(x):
        c1 = 'background-color: red'
        c2 = 'background-color: yellow'

        df1 = pd.DataFrame('', index=x.index, columns=x.columns)
        m = nn_df["Title"].str.contains("samsung")
        df1['Title'] = np.where(m, c1, c2)

        n = nn_df["Description"].str.contains("samsung")
        df1['Description'] = np.where(n, c1, c2)
        return df1

    nn_df.style.apply(expired, axis=None).to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/Youtube_Engagement.xlsx',index=False)

    # nn_df.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/Youtube_Engagement.xlsx',index=False)

    return nnn_df