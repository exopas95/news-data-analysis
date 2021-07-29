# KIM & CHANG Project

## News Data Crawling
Collected news data using Naver Search API
- [Naver Open API URL](https://developers.naver.com/products/service-api/search/search.md)

Data collceted using following keywords
- CEO: 서경배, 김동관, 이재현, 서정진, 조현준, 김정태, 최정우, 박정호, 정호영, 한성숙
- Company: 아모레퍼시픽, 한화, CJ, 셀트리온, 효성, 하나금융, 포스코, SKT, LG디스플레이, 네이버

Additional Keyword Conditions
- Negative: 특혜, 비판, 비난, 논란, 패륜, 후계, 승계, 세습, 경영권분쟁 etc...
- Prosecution: 재판, 공판, 소송, 법원, 판결, 선고, 사법리스크, 기소, 수사, 고발 etc...
- Congress: 기자회견, 토론회, 청문회, 국정감사, 국감, 소환, 진상조사, 개정 etc...
- Fair Trade Commission(공정거래위원회): 공정위, 공정거래위원회, 불공정거래, 일감몰아주기
- Financial Authorities: 금융위, 금감원, 금융감독원, 금융위원회, 금융당국 etc...

Please check apiKeyword.py for further keyword conditions

## DART Data Crawling
Collected company information from DART
- [DART Open API URL](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001)

Company list
- 삼성전자, 한화, 아모레퍼시픽, CJ, 셀트리온
- 효성, 하나금융지주, 포스코, SK텔레콤, LG디스플레이
- NAVER, 깨끗한나라, 대우부품, 대유에이텍, 대창단조
- 동서, 동양피스톤, 두산퓨얼셀, 디아이씨, 보령제약
- 부산산업, 삼천리, 상신브레이크, 새론오토모티브, 서연이화
- 성신양회, 세아제강, 신성통상, 애경산업, 종근당
- 하이트진로, 남양유업, 코오롱, 오리온, 웅진
- 카카오, 교촌에프앤비, 케이티앤지, 한샘, 포스코케미칼
- 우리금융지주, KB금융, 넥센, 농심, 대한항공
- 동국제강, 두산, 하이브, 엔씨소프트, 오뚜기
- 현대백화점, 현대자동차, 호텔신라, GS, 한국조선해양

## DART Network Analysis
Network Analysis based on DART company disclosure information
Analysis is only based on their Education and Career history

### Graph Analysis
[NetworkX](https://networkx.org/) is used for graph analysis
Calculated individual betweenness / closeness / cetrality / eigenvector / pagerank
- Betweeness(btw): 노드 간의 최단 경로에서 얼마나 빈번하게 해당 노드를 지나가는지를 평가
- Closeness(cls): 다른 노드까지의 평균 거리를 평가
- Centrality(dgr): 한 노드에 연결된 모든 Edge의 개수로 중심성 평가
- Eigenvector(egv): 중요한 노드와 많이 연결됬는지를 평가 (Centrality 단점 보완)
- PageRank(pgr): 한 노드의 영향력이 다른 노드에 미치는 것을 방지하여 노드의 중요도 평가

## Usage
### News Data Crawling
Get Open API Key from the official website and change the key value from `apiCrawler.py`
```python
    YOUR_CLIENT_ID = ""
    YOUR_CLIENT_SECRET = ""
```

Then run `python main.py` to execute the code

### DART Data Crawling
Get Open API Key from the official website and change the key value from `dartCrawler.py`
```python
api_key = ''
```
You can modifiy the company list from `company_list`
Try not to change any column information if you want to use the file for network analysis
If you need to, please modify column information in `networkX.py` as well
As a result you will get a csv file name `dart_data_processed.csv`

Then run `python dartCrawler.py` to execute the code

### DART Network Analysis

Run `python networkX.py` to execute the code
