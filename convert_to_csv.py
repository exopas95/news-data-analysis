import pandas as pd
import numpy as np
import json

from datetime import datetime as dt

with open('/home/treenulbo/Develop/kim_and_chang_nlp/data/crawler_result_2021-04-23 03:11:53.374270.json', encoding='utf-8-sig') as f:
    data = json.load(f)

df = pd.DataFrame(data)

df = df.drop_duplicates().reset_index(drop=True)

df.title = df.title.apply(lambda x: x.replace('<b>', ''))
df.title = df.title.apply(lambda x: x.replace('</b>', ''))
df.title = df.title.apply(lambda x: x.replace('\n', ''))

df.description = df.description.apply(lambda x: x.replace('<b>', ''))
df.description = df.description.apply(lambda x: x.replace('</b>', ''))
df.description = df.description.apply(lambda x: x.replace('\n', ''))

df.pubDate = df.pubDate.apply(lambda x: x[5:16])
df.pubDate = df.pubDate.apply(lambda x: dt.strptime(x, '%d %b %Y').strftime('%Y-%m-%d'))

result = df[['pubDate', 'title', 'description']].sort_values('pubDate', ascending=False).reset_index(drop=True).copy()
# result.to_csv('data/crarwler_result_labeling.csv', encoding='utf
# -8-sig')

result_sample = result[result.pubDate <= '2018-01-01'].sample(n=200000).sort_values('pubDate', ascending=False).reset_index(drop=True)

for i in range(4):
    start = i * 5000
    end = (i + 1) * 5000

    result_sample.iloc[start:end, :].to_csv(f'data/crarwler_result_sample_labeling_{i}.csv', encoding='utf-8-sig')
