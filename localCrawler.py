# -*- coding: utf-8 -*-

import requests, re
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)  # dataframe print 할 때 전체 column 보기 위해서 추가
hangul = re.compile('[^ .,0-9ㄱ-ㅣ가-힣]+')  # 한글, 숫자, 마침표, 쉼표, 공백만

# header 의 cookie 에 넣을 언론사 코드
pressDict = {'조선일보': 1023, '중앙일보': 1025, '동아일보': 1020, '한국일보': 1469, '서울신문': 1081, '국민일보': 1005, '세계일보': 1022, '경향신문': 1032, '한겨레': 1028, '문화일보': 1021, 'KBS': 1056, 'MBC': 1214, 'SBS': 1055, 'TV조선': 1448, '채널A': 1449, 'JTBC': 1437, 'MBN': 1019, '연합뉴스TV': 1422, 'YTN': 1052, '한국경제TV': 1004, '한국경제': 1015, '매일경제': 1009, '서울경제': 1011, '머니투데이': 1008, '아시아경제': 1277, '헤럴드경제': 1016, '파이낸셜뉴스': 1014, '이데일리': 1018, '조선비즈': 1366, '연합뉴스': 1001, '뉴시스': 1003, '뉴스1': 1421, '노컷뉴스': 1079, '오마이뉴스': 1047}
# 'SBS CNBC': '없음'  # SBS CNBC는 존재하지 않음

# 검색할 키워드 리스트
searchKeywords = ['아모레퍼시픽 서경배', '한화 김동관', 'CJ 이재현', '셀트리온 서정진', '효성 조현준', '하나금융 김정태', '포스코 최정우', 'SKT 박정호', 'LG디스플레이 정호영', '네이버 한성숙']
cnt = 1

df = pd.DataFrame(columns=['pressName', 'ceoName', 'newsTitle', 'url', 'date', 'article'])  # 저장할 데이터. 데이터프레임 형태
for searchKeyword in searchKeywords:  # 각 검색어 키워드 마다
    print(searchKeyword)
    for pressID in pressDict:  # 언론사별로
        # df = pd.DataFrame(columns=['pressName', 'ceoName', 'newsTitle', 'url', 'date', 'article'])
        print(pressID)
        num = 1  # 검색 start를 위한 변수. 10씩 증가.
        breaker = False  # 10개 씩 넘기다가 더 이상 결과가 없으면 멈추기 위한 변수
        # header에 User-Agent 정보와 검색하고자 하는 언론사 코드를 넣어줌
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'cookie': f'news_office_checked={pressDict[pressID]};'
        }

        while not breaker:
            linkUri = f'https://search.naver.com/search.naver?where=news&query={searchKeyword}&sm=tab_opt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=1&start={num}&refresh_start=0&related=0'
            req = requests.get(linkUri, headers=headers)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            titles = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a')
            URIs = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div > a:nth-last-child(1)')

            if not titles:
                breaker = True

            for title, URI in zip(titles, URIs):
                print(cnt)
                headers2 = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                }
                req2 = requests.get(URI['href'], headers=headers2)
                html2 = req2.text
                soup2 = BeautifulSoup(html2, 'html.parser')
                try:
                    # 일반 뉴스
                    # 정규표현식으로 한글, 숫자, 마침표, 쉼표, 공백만 들고 올 때
                    # article = hangul.sub('', soup2.select('#articleBodyContents')[0].get_text())
                    # 그냥 다 들고 올 때. br 태그를 바꿔주지 않으면 단어가 붙는 현상이 발생해서 공백으로 바꿨다가 get_text() 적용
                    article = BeautifulSoup(str(soup2.select('#articleBodyContents')[0]).replace('<br>', ' '), 'html.parser').get_text()
                except:
                    try:
                        # 연예 뉴스
                        article = BeautifulSoup(str(soup2.select('#articeBody')[0]).replace('<br/>', ' '), 'html.parser').get_text()
                    except:
                        try:
                            # 스포츠 뉴스
                            article = BeautifulSoup(str(soup2.select('#newsEndContents')[0]).replace('<br>', ' '), 'html.parser').get_text()
                        except:
                            article = ''
                try:
                    # 일반 뉴스
                    date = soup2.select('#main_content > div.article_header > div.article_info > div > span.t11')[0].text.split(' ')[0]
                except:
                    try:
                        # 연예 뉴스
                        date = soup2.select('#content > div.end_ct > div > div.article_info > span > em')[0].text.split(' ')[0]
                    except:
                        try:
                            # 스포츠 뉴스
                            date = soup2.select('#content > div > div.content > div > div.news_headline > div > span:nth-child(1)')[0].text.split(' ')[1]
                        except:
                            date = ''

                temp = [pressID, searchKeyword.split(' ')[1], title['title'], URI['href'], date, article]

                df = df.append(pd.Series(temp, index=df.columns), ignore_index=True)
                # time.sleep(0.5)
                cnt += 1
            num += 10

df.to_pickle('naverNewsData.pickle')

# 정규표현식을 사용하지 않으면 utf-8-sig 로 저장 중에 오류 발생.
# df.to_csv(f"naverNewsData.csv", index=False, header=False, mode='a',encoding='utf-8-sig')
