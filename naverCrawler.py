import requests
import json
from urllib.parse import quote

# API KEY  
YOUR_CLIENT_ID = "xxx"
YOUR_CLIENT_SECRET = "xxx

# Naver API call
def call(keyword, start):
    encText = quote(keyword)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=100" + "&start=" + str(start)
    result = requests.get(url=url, headers={"X-Naver-Client-Id": YOUR_CLIENT_ID,
                                            "X-Naver-Client-Secret": YOUR_CLIENT_SECRET})
    print(result)  # Response [200]
    return result.json()
 
# Get 1,000 results
def get_results(keyword):
    temp_list = []
    for num in range(0, 10):
        temp_list = temp_list + call(keyword, num * 100 + 1)['items'] # list 안에 키값이 ’item’인 애들만 넣기
    return temp_list

result_list = []
searchKeywords = ['아모레퍼시픽 서경배', '한화 김동관', 'CJ 이재현', '셀트리온 서정진', '효성 조현준', '하나금융 김정태', '포스코 최정우', 'SKT 박정호', 'LG디스플레이 정호영', '네이버 한성숙']

for keywords in searchKeywords:
    result = get_results(keywords)
    result_list += result
 
file = open("./data/crawler_result.json", "w+", encoding='UTF-8-sig')  # gangnam.json 파일을 쓰기 가능한 상태로 열기 (만들기)
file.write(json.dumps(result_list, ensure_ascii=False))  # 쓰기