import pandas as pd
import numpy as np
from typing import List
from textrankr import TextRank
from konlpy.tag import Okt

class OktTokenizer:
    okt: Okt = Okt()

    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens

df = pd.read_csv('data/naverNewsData_final.csv')
df.columns = ['Press', 'Name', 'Title', 'Link', 'Date', 'Content']

content_list = df.Content

mytokenizer: OktTokenizer = OktTokenizer()
textrank: TextRank = TextRank(mytokenizer)

k: int = 3  # num sentences in the resulting summary
result_list = []

# if verbose = False, it returns a list
for content in content_list[:5]:
    summaries: List[str] = textrank.summarize(content, k, verbose=False)
    result = '. '.join(summaries)
    result_list.append(result)

print(result_list)
# df['Summarized'] = result_list
# df.to_csv('naverNewsData.csv', index=False, header=True, encoding='utf-8-sig')
