import requests
import json
import datetime
import apiKeyword

from urllib.parse import quote

# Naver API call
def call(keyword, display=10, start=1):
    # API KEY  
    YOUR_CLIENT_ID = "LhQ0m10Z5peIimi7oIue"
    YOUR_CLIENT_SECRET = "d5EWrGTaPw"

    encText = quote(keyword)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + f"&display={display}" + f"&start={str(start)}" 
    result = requests.get(url=url, headers={"X-Naver-Client-Id": YOUR_CLIENT_ID,
                                            "X-Naver-Client-Secret": YOUR_CLIENT_SECRET})
    # print(result)  # Response [200]
    return result.json()
 
# 처음 모든 history 데이터를 얻기 위해 사용합니다. - Get 1,000 results
def get_results(keyword):
    temp_list = []
    for num in range(0, 10):
        try:
            temp_list = temp_list + call(keyword, display=100, start=num * 100 + 1)['items'] # list 안에 키값이 ’item’인 애들만 넣기
        except:
            print('Data not found...')
            return temp_list
    return temp_list

# 최근 데이터를 사용할 때 사용합니다.
# def get_results(keyword):
#     result = []
#     result.append(call(keyword, display=100))
#     return result

def run():

    result_list = []
    searchKeywords = apiKeyword.get_keyword_list()

    # tqdm should be added
    num = 0
    for keywords in searchKeywords:
        result = get_results(keywords)
        result_list += result
        print(f'Processing {num} / {len(searchKeywords)}')
        num += 1
    
    now = datetime.datetime.now()
    file = open(f"./data/crawler_result_{now}.json", "w+", encoding='UTF-8-sig')  # gangnam.json 파일을 쓰기 가능한 상태로 열기 (만들기)
    file.write(json.dumps(result_list, ensure_ascii=False))  # 쓰기