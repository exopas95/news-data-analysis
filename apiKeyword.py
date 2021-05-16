
def make_keyword(subject_dict, person_dict, addition_keyword_1='', addition_keyword_2=''):
    result = []
    for person in person_dict:
        for subject in subject_dict:
            result.append(subject + addition_keyword_1 + ' + ' + person + addition_keyword_2)
    return result

def make_keyword_dict(): 
    keyword_ceo = ['서경배', '김동관', '이재현', '서정진', '조현준', '김정태', '최정우', '박정호', '정호영', '한성숙']
    keyword_company = ['아모레퍼시픽', '한화', 'CJ', '셀트리온', '효성', '하나금융', '포스코', 'SKT', 'LG디스플레이', '네이버']
    keyowrd_ceo_company = ['아모레퍼시픽 서경배', '한화 김동관', 'CJ 이재현', '셀트리온 서정진', '효성 조현준', '하나금융 김정태', '포스코 최정우', 'SKT 박정호', 'LG디스플레이 정호영', '네이버 한성숙']

    # 주제 키워드
    keyword_condition = {
        'keyword_1' : {
            'case_1': ['특혜', '비판', '비난', '논란', '패륜', '후계', '승계', '세습', '경영권분쟁'],
            'case_2': ['특혜', '비판', '비난', '논란', '패륜', '후계', '승계', '세습', '경영권분쟁'],
            'case_3': ['지배구조', '급여', '연봉', '횡령', '배임' '탈세'],
            'case_4': ['우려', '난관', '반대', '사퇴', '부진'],
            'case_5': ['최악', '위기', '과제', '부진', '악재', '노사', '오너리스크'],
            'case_6': ['갑질', '폭언', '폭행', '이혼', '구설', '루머', '물의', '난동', '음주', '협박', '괴롭힘']
        },
        # 재판 이슈
        'keyword_2' : {
            'case_1': ['재판', '공판', '소송', '법원', '판결', '선고', '사법리스크'],
            'case_2': ['재판', '공판', '소송', '법원', '판결', '선고', '사법리스크']
        },
        # 검찰, 경찰 조사 이슈
        'keyword_3' : {
            'case_1': ['기소', '수사', '고발', '고소', '소환', '공소', '구속', '영장', '입건', '체포'],
            'case_2': ['검찰', '경찰'],
            'case_3': ['압수수색'],
            'case_4': ['압수수색'],
            'case_5': ['기소', '수사', '고발', '고소', '소환', '공소', '구속', '영장', '입건', '체포']
        },
        # 국회 관련 이슈
        'keyword_4' : {
            'case_1': ['기자회견', '토론회', '청문회', '국정감사', '국감', '증인', '추궁', '소환', '진상조사'],
            'case_2': ['기자회견', '토론회', '청문회', '국정감사', '국감', '증인', '추궁', '소환', '진상조사'],
            'case_3': ['사익편취', '총수', '재벌', '통과', '입법', '상정' '감시', '의결', '감독', '개정'],
            'case_4': ['사익편취', '총수', '재벌', '통과', '입법', '상정' '감시', '의결', '감독', '개정'],
            'case_5': ['기자회견', '토론회', '청문회', '국정감사', '국감', '증인', '추궁', '소환', '진상조사'],
            'case_6': ['기자회견', '토론회', '청문회', '국정감사', '국감', '증인', '추궁', '소환', '진상조사'],
            'case_7': ['사익편취', '총수', '재벌', '통과', '입법', '상정' '감시', '의결', '감독', '개정'],
            'case_8': ['사익편취', '총수', '재벌', '통과', '입법', '상정' '감시', '의결', '감독', '개정']
        },
        # 공정위 관련 이슈
        'keyword_5' : {
            'case_1': ['공정위', '공정거래위원회', '불공정거래', '일감몰아주기']
        },
        # 금융당국 관련 이슈
        'keyword_6' : {
            'case_1': ['금융위', '금감원', '금융감독원', '금융위원회', '금융당국', '과세당국', '국세청'],
            'case_2': ['세무조사', '탈세', "분식회계"]
        },
        # 주요 정부부처 관련
        'keyword_7' : {
            'case_1': ['중소기업벤처부', '환경부', '고용노동부', '청와대']
        },
        # 사건 사고 이슈
        'keyword_8' : {
            'case_1': ['산업재해', '사망', '부상', '중상'],
            'case_2': ['논란', '의혹', '불공정거래', '사건', '사고', '중대재해', '직업병', '괴롭힘', '갑질']
        },
        # 소비자 사고 이슈
        'keyword_9' : {
            'case_1': ['블랙컨슈머', '민원', '고발', '분쟁', '리콜'],
            'case_2': ['유해물질', '정보유출', '집단소송', '손해배상', '위해정보'],
            'case_3': ['한국소비자원']
        },
        # 국민 권익위 현안
        'keyword_10' : {
            'case_1': ['국민권익위'],
            'case_2': ['부패행위', '복지부정', '공익침해', '행동강령', '부정청탁'],
            'case_3': ['고충처리', '이해충돌', '부패방지', '행정심판', '불공정거래']
        },
        # 노조 관련 현안
        'keyword_11' : {
            'case_1': ['구조조정', '단체교섭', '해고', '파업', '쟁의'],
            'case_2': ['노조']
        },
        # 인수 합병 현황
        'keyword_12' : {
            'case_1': ['M&A', '인수합병', '기업결함', '기업인수', '기업합병'],
            'case_2': ['결합금지', '결합승인', '결합심사', '독과점', '매각명령'],
            'case_3': ['매각공고', '인수의향서', '예비실사', '현장실사', '우선협상대상', '영업양수도계약'],
            'case_4': ['자산취득', '자산매각', '분리설립', '분할설립', '자산인수', '주식인수', '흡수합병', '신설합병', '역합병']
        },
        # 경영 실적 동향/전망
        'keyword_13' : {
            'case_1': ['경영실적', '경영전망', '경영동향', '경영동정'],
            'case_2': ['기업동향', '업계동향', '일일동향'],
            'case_3': ['실적분석', '실적전망']
        },
        # 증권사 리포트
        'keyword_14' : {
            'case_1': ['증권사리포트']
        },
        # NGO 실적 동향 전망
        'keyword_15' : {
            'case_1': ['시민단체']
        }
    }

    return keyword_ceo, keyword_company, keyowrd_ceo_company, keyword_condition

def get_keyword_list():

    keyword_ceo, keyword_company, keyowrd_ceo_company, keyword_condition = make_keyword_dict()

    keyword1 = make_keyword(keyword_condition['keyword_1']['case_1'], keyowrd_ceo_company)
    keyword2 = make_keyword(keyword_condition['keyword_1']['case_2'], keyword_company, addition_keyword_2=' + 일가')
    keyword3 = make_keyword(keyword_condition['keyword_1']['case_3'], keyowrd_ceo_company)
    keyword4 = make_keyword(keyword_condition['keyword_1']['case_4'], keyword_ceo, addition_keyword_1 = ' + 연임')
    keyword5 = make_keyword(keyword_condition['keyword_1']['case_5'], keyowrd_ceo_company)
    keyword6 = make_keyword(keyword_condition['keyword_1']['case_6'], keyowrd_ceo_company)

    keyword7 = make_keyword(keyword_condition['keyword_2']['case_1'], keyowrd_ceo_company)
    keyword8 = make_keyword(keyword_condition['keyword_2']['case_2'], keyword_company)

    keyword9 = make_keyword(keyword_condition['keyword_3']['case_1'], keyword_ceo)
    keyword10 = make_keyword(keyword_condition['keyword_3']['case_2'], keyowrd_ceo_company)
    keyword11 = make_keyword(keyword_condition['keyword_3']['case_3'], keyowrd_ceo_company)
    keyword12 = make_keyword(keyword_condition['keyword_3']['case_4'], keyword_company)
    keyword13 = make_keyword(keyword_condition['keyword_3']['case_5'], keyword_company)

    keyword14 = make_keyword(keyword_condition['keyword_4']['case_1'], keyword_ceo, addition_keyword_1 = ' + 의원')
    keyword15 = make_keyword(keyword_condition['keyword_4']['case_2'], keyword_ceo, addition_keyword_1 = ' + 국회')
    keyword16 = make_keyword(keyword_condition['keyword_4']['case_3'], keyword_ceo, addition_keyword_1 = ' + 국회')
    keyword17 = make_keyword(keyword_condition['keyword_4']['case_4'], keyword_ceo, addition_keyword_1 = ' + 의원')
    keyword18 = make_keyword(keyword_condition['keyword_4']['case_5'], keyword_company, addition_keyword_1 = ' + 의원')
    keyword19 = make_keyword(keyword_condition['keyword_4']['case_6'], keyword_company, addition_keyword_1 = ' + 국회')
    keyword20 = make_keyword(keyword_condition['keyword_4']['case_7'], keyword_company, addition_keyword_1 = ' + 국회')
    keyword21 = make_keyword(keyword_condition['keyword_4']['case_8'], keyword_company, addition_keyword_1 = ' + 의원')

    keyword22 = make_keyword(keyword_condition['keyword_5']['case_1'], keyword_company)

    keyword23 = make_keyword(keyword_condition['keyword_6']['case_1'], keyword_company)
    keyword24 = make_keyword(keyword_condition['keyword_6']['case_2'], keyword_company)

    keyword25 = make_keyword(keyword_condition['keyword_7']['case_1'], keyword_company)

    keyword26 = make_keyword(keyword_condition['keyword_8']['case_1'], keyword_company)
    keyword27 = make_keyword(keyword_condition['keyword_8']['case_2'], keyword_company)

    keyword28 = make_keyword(keyword_condition['keyword_9']['case_1'], keyword_company, addition_keyword_1 = ' + 소비자')
    keyword29 = make_keyword(keyword_condition['keyword_9']['case_2'], keyword_company, addition_keyword_1 = ' + 소비자')
    keyword30 = make_keyword(keyword_condition['keyword_9']['case_3'], keyword_company)

    keyword31 = make_keyword(keyword_condition['keyword_10']['case_1'], keyword_company)
    keyword32 = make_keyword(keyword_condition['keyword_10']['case_2'], keyword_company, addition_keyword_1 = ' + 국민권익위')
    keyword33 = make_keyword(keyword_condition['keyword_10']['case_3'], keyword_company, addition_keyword_1 = ' + 국민권익위')

    keyword34 = make_keyword(keyword_condition['keyword_11']['case_1'], keyword_company, addition_keyword_1 = ' + 노조')
    keyword35 = make_keyword(keyword_condition['keyword_11']['case_2'], keyword_company)

    keyword36 = make_keyword(keyword_condition['keyword_12']['case_1'], keyword_company)
    keyword37 = make_keyword(keyword_condition['keyword_12']['case_2'], keyword_company, addition_keyword_1 = ' + 공정위')
    keyword38 = make_keyword(keyword_condition['keyword_12']['case_3'], keyword_company)
    keyword39 = make_keyword(keyword_condition['keyword_12']['case_4'], keyword_company)

    keyword40 = make_keyword(keyword_condition['keyword_13']['case_1'], keyword_company)
    keyword41 = make_keyword(keyword_condition['keyword_13']['case_2'], keyword_company)
    keyword42 = make_keyword(keyword_condition['keyword_13']['case_3'], keyword_company)

    keyword43 = make_keyword(keyword_condition['keyword_14']['case_1'], keyword_company)

    keyword44 = make_keyword(keyword_condition['keyword_15']['case_1'], keyword_company)

    result = keyword1 + \
             keyword2 + \
             keyword3 + \
             keyword4 + \
             keyword5 + \
             keyword6 + \
             keyword7 + \
             keyword8 + \
             keyword9 + \
             keyword10 + \
             keyword11 + \
             keyword12 + \
             keyword13 + \
             keyword14 + \
             keyword15 + \
             keyword16 + \
             keyword17 + \
             keyword18 + \
             keyword19 + \
             keyword20 + \
             keyword21 + \
             keyword22 + \
             keyword23 + \
             keyword24 + \
             keyword25 + \
             keyword26 + \
             keyword27 + \
             keyword28 + \
             keyword29 + \
             keyword30 + \
             keyword31 + \
             keyword32 + \
             keyword33 + \
             keyword34 + \
             keyword35 + \
             keyword36 + \
             keyword37 + \
             keyword38 + \
             keyword39 + \
             keyword40 + \
             keyword41 + \
             keyword42 + \
             keyword43 
             
    return result