import pandas as pd
import numpy as np
import time as t
import warnings
warnings.filterwarnings('ignore')

tx = t.localtime()
timestamp = t.strftime('%b-%d-%Y_%H%M', tx)


def nps(df,result_df):
    nn_df = df.groupby(['Video_id', 'New Sentiment']).agg({"New Sentiment": ["count"]}).reset_index()
    nn_df.columns = nn_df.columns.droplevel(1)
    nn_df.columns = ['Video_id', 'New Sentiment', 'Count']
    nn_df['NPS'] = ''

    for i in range(0, len(nn_df), 3):
        nn_df['NPS'][i] = round((nn_df['Count'][i + 2] - nn_df['Count'][i]) / (
                nn_df['Count'][i] + nn_df['Count'][i + 1] + nn_df['Count'][i + 2]), 2)
        print(nn_df['Video_id'][i])

    nn_df = nn_df[nn_df['NPS'] != '']
    nn_df = nn_df.reset_index()

    nn_df.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/NPS ' + timestamp + '.xlsx', index=False)

    df1 = result_df
    df1.sort_values(by=['video_id'], inplace=True)
    df1 = df1.reset_index(inplace=False)
    df1['NPS'] = ''
    df1.loc[df1.video_id == nn_df.Video_id, 'NPS'] = nn_df.NPS

    # result_df['NPS'] = ''
    # for i in range(0, len(result_df['video_id'])):
    #     for j in range(0, len(nn_df['Video_id'])):
    #         if result_df['video_id'][i] == nn_df['Video_id'][j]:
    #             # result_df['NPS'][i] = copy.copy(nn_df['NPS'][j])
    #             result_df['NPS'][i] = nn_df['NPS'][j]


    df1=df1[['IST','Title','Published_date','Views','Likes','Comments','Description','video_id','Channel_id','Channel_name','Video_Url','Type','NPS']]

    df1.to_excel('C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/Final ' + timestamp + '.xlsx', index=False)

    return df1