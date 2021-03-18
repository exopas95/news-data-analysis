# KIM & CHANG Project

## Data Crawling

Collected news data using BeautifulSoup

- Searched articles from Naver up to 2021.03.10.
- [DataFrame saved in a pickle file](https://drive.google.com/file/d/1c49c5rdJnVpeZ99u6MgEBfrK_bfnlOQW/view?usp=sharing)

  

## Text Summarization
Summarized crawled data using [textrankr](https://github.com/theeluwin/textrankr)
- Designed for Korean
- Available for Python3

### Requirements
- [textrankr](https://github.com/theeluwin/textrankr)
- [konlpy](https://konlpy.org/en/latest/install/)

### Usage
```Python
from typing import List
from textrankr import TextRank
from konlpy.tag import Okt

class OktTokenizer:
    okt: Okt = Okt()

    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens

mytokenizer: OktTokenizer = OktTokenizer()
textrank: TextRank = TextRank(mytokenizer)

k: int = 3  # num sentences in the resulting summary
result_list = []

# if verbose = False, it returns a list
for content in content_list:
    summaries: List[str] = textrank.summarize(content, k, verbose=False)
    result = '. '.join(summaries)
    result_list.append(result)
```
