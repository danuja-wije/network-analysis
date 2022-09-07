# install these libraries if you don't already have them
# !pip install facebook_scraper
# !pip install vaderSentiment
# !pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from collections.abc import Iterable
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
import spacy
from spacy.matcher import PhraseMatcher
import statsmodels.api as sm

df = pd.read_csv('facebook_data_sample_small.csv')

df = df.sample(frac=0.1)

df_post = pd.DataFrame()

columns = ['post_id',
           'comments']

df_post = pd.DataFrame(columns=columns)
df_post['post_id'] = df['post_id_x']
df_post['comments_full'] = df['message_y']
df_post['text'] = df['message_x']

posts = df_post.groupby(['post_id','comments_full']).agg({'text':'count'})

posts['post_id'] = posts.index.get_level_values(0)
posts['comment_full'] = posts.index.get_level_values(1)
posts['text'] = posts['text'].astype(int)
posts.reset_index(inplace=True,drop=True)

post_list = {}
comment_list = []

for line in df.itertuples():
    if line.post_id_x not in post_list:
        post_list[line.post_id_x] = [line.message_x]
    else:
        post_list[line.post_id_x].append(line.message_x)
    comment_list.append(line.message_x)

posts['all_comments'] = posts.apply(lambda x: post_list[x['post_id']], axis=1)

posts.dropna(inplace=True)

posts = posts.sample(frac=0.3)

analyzer = SentimentIntensityAnalyzer()

list_comments = []
for index, row in posts.iterrows():
    post_id = row['post_id']
    if isinstance(row['all_comments'], Iterable):
        for comment in row['all_comments']:
            dict_temp = {}
            dict_temp['post_id'] = post_id
            dict_temp['comment'] = len(row['all_comments'])
            dict_temp['sentiment'] = analyzer.polarity_scores(str(comment))['compound']
            list_comments.append(dict_temp)

df_comments = pd.DataFrame(list_comments)

posts_sentiment = df_comments.groupby('post_id').mean()

df_posts = df_post.join(posts_sentiment, on=['post_id'])

df_posts.drop(columns=['comments_full'], inplace=True)
df_posts.fillna(0.0, inplace=True)

# merge all texts in posts
post_text = str(df_posts['text'])
post_text = post_text.replace('\n', '') # remove blank lines characters

# update stopwords
stopwords = set(STOPWORDS)
stopwords.update(['https', 'gov', 'au', 'nsw', 's', 're'])

# Generate a word cloud image
wordcloud = WordCloud(random_state=1,
                      collocations=True,
                      stopwords=stopwords,
                      max_words=120,
                      background_color='black',
                      colormap ='rainbow',
                      contour_color='steelblue').generate(post_text)

plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
plt.savefig('Plotly-World_Cloud.png')

