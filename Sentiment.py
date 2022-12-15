from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd
# import warnings
# warnings.filterwarnings('ignore')
import time as t

tx = t.localtime()
timestamp = t.strftime('%b-%d-%Y_%H%M', tx)

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)


def sentiment(df):
    df['Text Length'] = df['Text'].str.len()
    df['New Sentiment'] = ''

    n_df = df[df['Text Length'] > 1000]
    n_df = n_df.reset_index()
    n_df['New Sentiment'] = "Neutral"

    df = df[df['Text Length'] <= 1000]
    df = df.reset_index()

    for i in range(0, len(df)):
        try:

            tweet = df['Text'][i]

            # precprcess tweet
            tweet_words = []

            for word in tweet.split(' '):
                if word.startswith('@') and len(word) > 1:
                    word = '@user'

                elif word.startswith('http'):
                    word = "http"
                tweet_words.append(word)

            tweet_proc = " ".join(tweet_words)

            labels = ['Negative', 'Neutral', 'Positive']

            # sentiment analysis
            encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
            # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
            output = model(**encoded_tweet)

            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            #     df['New Sentiment'][i]=labels[pd.Series(scores).idxmax()]

            if max(scores) >= 0.80 and labels[pd.Series(scores).idxmax()] == "Positive":
                df['New Sentiment'][i] = "Positive"
            elif max(scores) >= 0.75 and labels[pd.Series(scores).idxmax()] == "Negative":
                df['New Sentiment'][i] = "Negative"
            else:
                df['New Sentiment'][i] = "Neutral"

            print(i)
            print(df['New Sentiment'][i])

            # for i in range(len(scores)):
            #     l = labels[i]
            #     s = scores[i]
            #     print(l, s)

        except:
            df['New Sentiment'][i] = "Neutral"
            pass
    df = pd.concat([df, n_df], axis=0)

    df.to_excel(
        'C:/Users/shivkant.s/Desktop/YT_new/Daily YT Data/YT Comments Analysis ' + timestamp + '.xlsx',
        index=False)

    return df
