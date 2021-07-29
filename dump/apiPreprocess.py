import pandas as pd
import numpy as np
import pickle
import re
import hanja
from pykospacing import spacing

'''
Pre-requisite
!pip install hanja
!pip install tensorflow
!pip install git+https://github.com/haven-jeon/PyKoSpacing.git
​'''

def pre(text):
    # 불필요한 문자 제거 및 대체
    punct = {'…':'...',
            '“':'"', '”':'"',
            "‘":"'", "’":"'",
            "‘":"'", "’":"'",
            '\t':'', '\n':'', 
            '/':'',
            '▲':'', '■':'', '●':'', '○':''}
    for p in punct:
        text = text.replace(p, punct[p])

    # 한자어 변환
    text = hanja.translate(text, 'substitution')

    # 기사와 무관한 내용 제거
    text = text.rsplit('기자', 1)[0]
    text = text.rsplit('.', 1)[0]+'.'
    text = text.split('▶')[0]
    # 추가 필요
    text = text.replace("[동아닷컴]",'').replace("[동아일보]",'').replace("[서울신문]",'').replace("[서울Biz]",'').replace("[세계파이낸스]",'')

    # 띄어쓰기 교정
    text = text.replace(" ", '')
    text = spacing(text)

    return text

def pre_run():
    with open('data/naverNewsData.pickle','rb') as f:
        data = pickle.load(f)

    temp_list = []

    for content in data['article']:
        temp_list.append(pre(content))

    data['revisedArticle'] = temp_list
    
    return data