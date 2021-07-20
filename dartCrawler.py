# %%
import requests
from io import BytesIO
from zipfile import ZipFile
from xml.etree.ElementTree import parse
import pandas as pd

# %%
############################## 크롤링 코드 ##############################
api_key = ''
url = 'https://opendart.fss.or.kr/api/corpCode.xml'
params = {'crtfc_key': api_key}
r = requests.get(url, params)
filename = 'corpCode'

# 바이너리 io 진행 + zip 파일 압축해제 export
with ZipFile(BytesIO(r.content)) as zipfile:
    zipfile.extractall(filename)

    
# xml 파일 파싱
doc = parse(f"{filename}/CORPCODE.xml")

# root는 xml 문서의 최상단 루트 태그를 가리킴
root = doc.getroot()

# 태그별로 필요한 정보를 찾아 파싱하여 딕셔너리의 키, 값의 쌍으로 저장
rows = []

for node in root:
    n_corp_code = node.findtext('corp_code')
    n_corp_name = node.findtext('corp_name')
    n_stock_code = node.findtext('stock_code')
    n_modify_date = node.findtext('modify_date')
    rows.append({"corpCode": n_corp_code,
                 "corpName": n_corp_name,
                 "stockCode": n_stock_code,
                 "modifyDate": n_modify_date})

columns = ["corpCode", "corpName", "stockCode", "modifyDate"]
corpInfo = pd.DataFrame(rows, columns = columns)
corpInfo = corpInfo[corpInfo['stockCode'] != ' ']
corpInfo = corpInfo.astype({'corpCode': int})
corpInfo['modifyDate'] = pd.to_datetime(corpInfo['modifyDate'])
corpInfo = corpInfo.sort_values('modifyDate').drop_duplicates('corpName', keep='last').reset_index(drop=True)

# %%
# 기업 리스트 - 세아제강
company_list = ['삼성전자', '한화', '아모레퍼시픽', 'CJ', '셀트리온',
                '효성', '하나금융지주', '포스코', 'SK텔레콤', 'LG디스플레이', 
                'NAVER', '깨끗한나라', '대우부품', '대유에이텍', '대창단조',
                '동서', '동양피스톤', '두산퓨얼셀', '디아이씨', '보령제약',
                '부산산업', '삼천리', '상신브레이크', '새론오토모티브', '서연이화',
                '성신양회', '세아제강', '신성통상', '애경산업', '종근당',
                '하이트진로', '남양유업', '코오롱' , '오리온', '웅진',
                '카카오', '교촌에프앤비', '케이티앤지', '한샘', '포스코케미칼',
                '우리금융지주', 'KB금융', '넥센', '농심', '대한항공',
                '동국제강', '두산', '하이브', '엔씨소프트', '오뚜기',
                '현대백화점', '현대자동차', '호텔신라', 'GS', '한국조선해양']

# company_list = ['세아제강', '신성통상', '애경산업', '종근당',
#                 '하이트진로', '남양유업', '코오롱' , '오리온', '웅진',
#                 '카카오', '교촌에프앤비', '케이티앤지', '한샘', '포스코케미칼',
#                 '우리금융지주', 'KB금융', '넥센', '농심', '대한항공',
#                 '동국제강', '두산', '하이브', '엔씨소프트', '오뚜기',
#                 '현대백화점', '현대자동차', '호텔신라', 'GS', '한국조선해양']

company = corpInfo[corpInfo['corpName'].isin(company_list)].reset_index(drop=True)
company.loc[:, 'corpCode'] = company.corpCode.map("{:08}".format)
# %%
bsnsYear = 2020     # 가장 최근 년도
reprtCode = 11011   # 사업보고서
corpCode = company.corpCode.to_list()
corpList = []

for corp in corpCode:
    try:
        # url 읽고 크롤링
        url = 'https://opendart.fss.or.kr/api/exctvSttus.json?crtfc_key=' + api_key + f"&corp_code={corp}" + f"&bsns_year={bsnsYear}" + f"&reprt_code={reprtCode}"
        r = requests.get(url)

        data = r.json()

        if data['status']=='000':
            for corp in data['list']:
                corpList.append({
                                'corp_name':corp['corp_name'],
                                'nm':corp['nm'],
                                'ofcps':corp['ofcps'],
                                'chrg_job':corp['chrg_job'],
                                'main_career':corp['main_career']})
    except:
        print("Data not found") 

# %%
columns = ['corp_name', 'nm', 'ofcps', 'chrg_job', 'main_career']
exctvInfo = pd.DataFrame(corpList, columns = columns)
exctvInfo.to_csv('data\dart_data_processed_3.csv', encoding='utf-8-sig')

# %%
############################## 전처리 코드 ##############################
# 세아제강
df1 = exctvInfo[exctvInfo.corp_name == '세아제강']
df1
# %%
# 신성통상
# 애경산업
# 종근당
# 하이트진로
# 남양유업
# 코오롱
# 오리온
# 웅진
# 카카오
# 교촌에프앤비
# 케이티앤지
# 한샘
# 포스코케미칼
# 우리금융지주
# KB금융
# 넥센
# 농심
# 대한항공
# 동국제강
# 두산
# 하이브
# 엔씨소프트
# 오뚜기
# 현대백화점
# 현대자동차
# 호텔신라
# GS
# 한국조선해양