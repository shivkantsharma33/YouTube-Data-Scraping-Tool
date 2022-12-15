import streamlit as st
import pandas as pd
import numpy as np
import datetime
import openpyxl
from YT_scrap import *
from Comments import *
from Sentiment import *
from NPS import *
import warnings
warnings.filterwarnings('ignore')


st.markdown("<h1 style='text-align: center; color: red;'>Youtube Data Scrapping Tool</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")

number = st.number_input('Enter No. of recent videos to extract', min_value=0, max_value=50, step=1)


if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file)
    # st.write(dataframe)


# number = st.number_input('Insert No. Of Videos', min_value=0, max_value=50, step=1)
# st.write('The current number is ', number)

# data=scrap(dataframe,number)

# data=pd.DataFrame()
s_date = st.date_input("Select Date From")
s_time = st.time_input('Select Time From', datetime.time(10, 00))

e_date = st.date_input("Select Date To")
e_time = st.time_input('Select Time To', datetime.time(10, 00))


s_date_time=str(s_date) +' '+ str(s_time)
e_date_time=str(e_date)+' '+str(e_time)

if st.button('Run'):
    placeholder = st.empty()

    data = scrap(dataframe, number)

    filter_data = datefilter(data, s_date_time, e_date_time)

    # placeholder.info('Comments Scrapping......')
    #
    # df_final = get_YT_subcount(filter_data['video_id'])
    #
    # placeholder.info('Comments Sentiment Analysis......')
    # comments_sentiment = sentiment(df_final)
    #
    # placeholder.info('NPS Calculation......')
    # NPS = nps(comments_sentiment,filter_data)
    #
    # st.write('Total :',len(comments_sentiment['New Sentiment']))
    # st.write(comments_sentiment['New Sentiment'].value_counts())

    placeholder.success('Congratulation...')

    st.balloons()
    # st.snow()










