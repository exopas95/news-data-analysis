import modin.pandas as pd
import numpy as np
import pickle
import re
import random
import hanja
import localSummarizer

from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Kkma
from konlpy.utils import pprint

def df1pre(text):
    # 불필요한 문자 제거 및 대체
    punct = {'…':'...',
            '“':'"', '”':'"',
            "‘":"'", "’":"'",
            "‘":"'", "’":"'",
            '\t':'', '\n':'', '\r':' ',
            '/':'',
            '▲':'', '■':'', '●':'', '○':'',
            '(사진)':'', '동영상 뉴스':''}
    for p in punct:
        text = text.replace(p, punct[p])

    # 한자어 변환
    text = hanja.translate(text, 'substitution')

    # 기사와 무관한 내용 제거
    text = text.rsplit('기자', 1)[0]
    text = text.rsplit('@', 1)[0]
    text = text.rsplit('.', 1)[0]+'.'
    text = text.split('▶')[0]
    text = text.split('☞')[0]
    text = text.split('[MBN')[0]
    text = text.split('[')[0]

    return text

def df2pre(text):
    # 불필요한 문자 제거 및 대체
    punct = {'…':'...',
            '“':'"', '”':'"',
            "‘":"'", "’":"'",
            "‘":"'", "’":"'",
            '\t':'', '\n':'', '\r':' ',
            '/':'',
            '▲':'', '■':'', '●':'', '○':'',
            '(사진)':''}
    for p in punct:
        text = text.replace(p, punct[p])


    # 한자어 변환
    text = hanja.translate(text, 'substitution')

    # 기사와 무관한 내용 제거
    text = text.rsplit('기자', 1)[0]
    text = text.rsplit('.', 1)[0]+'.'

    return text

def df3pre(text):
    # 불필요한 문자 제거 및 대체
    punct = {'…':'...',
           '“':'"', '”':'"',
           "‘":"'", "’":"'",
           "‘":"'", "’":"'",
           '\t':'', '\n':'', '\r':' ',
           '/':'',
           '▲':'', '■':'', '●':'', '○':'',
           '(사진)':'', '동영상 뉴스':''}
    for p in punct:
        text = text.replace(p, punct[p])

    # 한자어 변환
    text = hanja.translate(text, 'substitution')

    # 기사와 무관한 내용 제거
    text = text.rsplit('(영상', 1)[0]
    text = text.rsplit('@', 1)[0]
    text = text.rsplit('.', 1)[0]+'.'
    text = text.split('▶')[0]
    text = text.split('ⓒ')[0]
    text = text.rsplit('꿈을 담는 캔버스 채널A', 1)[0]

    return text

# print 해볼 때 전체 다 띄워보려고 쓰는 옵션
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', None)

with open("data/naverNewsData.pickle",'rb') as f:
    raw = pickle.load(f)

raw['date'] = pd.to_datetime(raw['date'])

# 과거 데이터의 경우 양식이 굉장히 다름
data = raw[raw['date']>='2017-01-01'].copy()

df1 = data[(data['pressName']!='MBC') &
            (data['pressName']!='채널A') &
            (data['pressName']!='JTBC')&
            (data['pressName']!='연합뉴스TV')&
            (data['pressName']!='YTN')].copy()

df1.reset_index(drop=True, inplace=True)
df1['revisedArticle'] = 0

for i in range(len(df1)):
    text = df1['article'][i]
    df1['revisedArticle'][i] = df1pre(text)

#### df2
df2=data[(data['pressName']=='MBC')].copy()
df2.reset_index(drop=True, inplace=True)
df2['revisedArticle']=0

for i in range(len(df2)):
    text = df2['article'][i]
    df2['revisedArticle'][i] = df2pre(text)

#### df3
df3 = data[(data['pressName']=='채널A')|
            (data['pressName']=='JTBC')|
            (data['pressName']=='연합뉴스TV')|
            (data['pressName']=='YTN')].copy()
df3.reset_index(drop=True, inplace=True)
df3['revisedArticle']=0

for i in range(len(df3)):
    text = df3['article'][i]
    df3['revisedArticle'][i] = df3pre(text)

revised_v1 = pd.concat([df1.drop(columns=['article']), df2.drop(columns=['article'])])
revised_v2 = pd.concat([revised_v1, df3.drop(columns=['article'])])
revised = localSummarizer.summarize(revised_v2)
revised.to_csv('data/local_data_preprocessed.csv', encoding='UTF-8-sig')

## 유사도 검사
# KB = revised[revised.ceoName=='서경배'].copy()
# KB.reset_index(drop=True, inplace=True)

# DK = revised[revised.ceoName=='김동관'].copy()
# DK.reset_index(drop=True, inplace=True)

# JaeH = revised[revised.ceoName=='이재현'].copy()
# JaeH.reset_index(drop=True, inplace=True)

# JJ = revised[revised.ceoName=='서정진'].copy()
# JJ.reset_index(drop=True, inplace=True)

# HJ = revised[revised.ceoName=='조현준'].copy()
# HJ.reset_index(drop=True, inplace=True)

# JT = revised[revised.ceoName=='김정태'].copy()
# JT.reset_index(drop=True, inplace=True)

# JW = revised[revised.ceoName=='최정우'].copy()
# JW.reset_index(drop=True, inplace=True)

# JungH = revised[revised.ceoName=='박정호'].copy()
# JungH.reset_index(drop=True, inplace=True)

# HY = revised[revised.ceoName=='정호영'].copy()
# HY.reset_index(drop=True, inplace=True)

# JS = revised[revised.ceoName=='한정숙'].copy()
# JS.reset_index(drop=True, inplace=True)

# #### 서경배
# mydoclist=KB['revisedArticle'].to_list()

# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''

#     for noun in nouns:
#         doc_nouns += noun + ' '

#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)

# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray = document_distances.toarray()
# revKB = KB.copy()
# cnt = 0

# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered) >= 2:
#         revKB.drop([i], inplace=True)
#         cnt += 1

# print(len(KB),"중",cnt,"개가 제거되어",len(revKB),"개가 남았습니다")

# #### 김동관
# mydoclist=DK['revisedArticle'].to_list()
# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''

#     for noun in nouns:
#         doc_nouns += noun + ' '

#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)
# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray = document_distances.toarray()

# revDK = DK.copy()
# cnt = 0

# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered)>=2:
#         revDK.drop([i], inplace=True)
#         cnt+=1

# print(len(DK),"중",cnt,"개가 제거되어",len(revDK),"개가 남았습니다")

# #### 이재현
# mydoclist=JaeH['revisedArticle'].to_list()

# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''

#     for noun in nouns:
#         doc_nouns += noun + ' '

#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)
# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray=document_distances.toarray()
# revJaeH = JaeH.copy()
# cnt = 0

# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered)>=2:
#         revJaeH.drop([i], inplace=True)
#         cnt+=1

# print(len(JaeH),"중",cnt,"개가 제거되어",len(revJaeH),"개가 남았습니다")

# revised[revised['pressName']=='조선일보']
# mydoclist=JJ['revisedArticle'].to_list()
# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''
    
#     for noun in nouns:
#         doc_nouns += noun + ' '
    
#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)
# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray=document_distances.toarray()

# revJJ=JJ.copy()
# cnt=0
# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered)>=2:
#         revJJ.drop([i], inplace=True)
#         cnt+=1

# print(len(JJ),"중",cnt,"개가 제거되어",len(revJJ),"개가 남았습니다")

# #### 조현준
# mydoclist=HJ['revisedArticle'].to_list()
# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''

#     for noun in nouns:
#         doc_nouns += noun + ' '
    
#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)
# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray = document_distances.toarray()
# revHJ = HJ.copy()

# cnt=0
# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered)>=2:
#         revHJ.drop([i], inplace=True)
#         cnt+=1

# print(len(HJ),"중",cnt,"개가 제거되어",len(revHJ),"개가 남았습니다")

# #### 김정태
# mydoclist=JT['revisedArticle'].to_list()
# kkma = Kkma()
# doc_nouns_list = []

# for doc in mydoclist:
#     nouns = kkma.nouns(doc)
#     doc_nouns = ''
    
#     for noun in nouns:
#         doc_nouns += noun + ' '
    
#     doc_nouns_list.append(doc_nouns)

# tfidf_vectorizer = TfidfVectorizer(min_df=1)
# tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)
# document_distances = (tfidf_matrix * tfidf_matrix.T)
# simArray = document_distances.toarray()

# revJT = JT.copy()
# cnt = 0

# for i in range(len(simArray)):
#     s = simArray[i,:]
#     filtered = list(filter(lambda x: x>=0.2, s))
#     if len(filtered) >= 2:
#         revJT.drop([i], inplace=True)
#         cnt += 1