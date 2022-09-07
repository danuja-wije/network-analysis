import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from community import community_louvain
from app import app
import random

file_path = "facebook_data_sample_small.csv"

df = pd.read_csv(file_path)
df = df[df['page_name'].isin(['cnn'])]
df_size = df.shape[0]

frack_p = 0.5
df_sampled = df.sample(frac=frack_p)
sample_size = df_sampled.shape[0]


page_list = {}
post_list = []

for line in df_sampled.itertuples():
    if line.page_name not in page_list:
        page_list[line.page_name] = [line.post_id_x]
    else:
        page_list[line.page_name].append(line.post_id_x)
    post_list.append(line.post_id_x)

G = nx.from_pandas_edgelist(df_sampled, source='post_id_x', target='from_id')

degree_size = list(dict(G.degree()).values())

degree_freq = Counter(degree_size)
degs, frq = zip(*degree_freq.items())

number_of_colors = len(df_sampled.groupby('page_name'))
pages = list(df_sampled.groupby('page_name').groups.keys())
color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]

colors = {}
i = 0
for c in color:
    colors[pages[i]] = c
    i += 1

node_col = {}
for d in list(dict(G.degree).keys()):
    if d in page_list['cnn']:
        node_col[d] = 'green'
    else:
        node_col[d] = 'blue'

node_color = [node_col.get(k) for k, v in dict(G.degree()).items()]
