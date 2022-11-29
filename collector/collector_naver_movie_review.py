# import math
#
# import requests
# from bs4 import BeautifulSoup
# import re
# import math
#
# ##################
# # 1. 영화 제목 수집 #
# ##################
#
# # movie_code : 네이버 영화 코드(6자리 숫자)
#
# # 제목 수집
# # 함수
# #  - 1.생성, 2.호출
# #  - 함수는 생성하면 아무 동작 X
# #  - 반드시 생성 후 호출을 통해서 사용!
#
#
# def movie_title_crawler(movie_code):
#     url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'
#     result = requests.get(url)
#     doc = BeautifulSoup(result.text, 'html.parser')
#     title = doc.select('h3.h_movie > a')[0].get_text()  # 자식인 a태그
#     return title
#
#
# # 리뷰 수집(리뷰, 평점, 작성자, 작성일자) + 제목
# def movie_review_crawler(movie_code):
#     title = movie_title_crawler(movie_code) # 제목 수집
#     print(f'>>Start collecting movies for {title}')
#
#     # set {제목, 리뷰, 평점, 작성자, 작성 일자}
#     url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
#     result = requests.get(url)
#     doc = BeautifulSoup(result.text, 'html.parser')
#     all_count = doc.select('strong.total > em')[0].get_text()  # 리뷰 전체 수
#     # "2,480" : str type(문자열)
#     # ex) 문자열 / 10 (X)
#     # int type(정수형 숫자)
#     # print(type(all_count))
#     # "2480" -> 2480 (O)
#     # "2,480" -> 문자 포함 변환(X)
#
#     # 1. 숫자만 추출 : 정규식
#     numbers = re.sub(r'[^0-9]', '', all_count)  # 0-9까지를 제외하고 다 ''으로 취급
#     pages = math.ceil(int(numbers)/10)  # 올림 ceil()
#     print(f'The total number of pages to collect is {pages}')
#     # 2480건 / 10
#     # 해당 페이지 리뷰 수집!
#     count = 0  # 전체 리뷰수를 count
#     for page in range(1, pages+1):  # 전체 페이지 리뷰 수집
#         url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
#         result = requests.get(url)
#         doc = BeautifulSoup(result.text, 'html.parser')
#         review_list = doc.select(('div.score_result > ul > li'))
#         for i, one in enumerate(review_list):
#             # 리뷰, 평점, 작성자, 작성 일자
#             score = one.select('div.star_score > em')[0].get_text()
#             review = one.select('div.score_reple > p > span')[-1].get_text().strip() #마지막 값 가져오기
#             # 전처리: 날짜 시간 -> 날짜만 추출
#             # -예: 2022.10.09 15:28 -> 2022.10.19
#             # - 날짜는 항상 16글자로 구성
#             original_date = one.select('div.score_reple dt > em')[1].get_text()
#             # 문자열 추출
#             # [시작:끝+1], 끝은 포함 X
#             # [:15] 0~14
#             # [3:] : 3~끝까지
#             date = original_date[:10]
#
#             original_writer = one.select('div.score_reple dt > em')[0].get_text().strip()
#             idx_end = original_writer.find('(')  # (의 인덱스번호
#             writer = original_writer[:idx_end]
#             count += 1
#
#             print(f"################# 리뷰-> {count}개 #################")
#             print(f'# Review: {review}')
#             print(f'# Score: {score}')
#             print(f'# Date: {date}')
#             print(f'# writer: {writer}')
#
#     return review_list
#
##################
# 영화 제목 수집
##################
import math
import requests
from bs4 import BeautifulSoup
import re
from db.database import create_review


# movie_code : 네이버 영화 코드(6자리 숫자)
# 함수 생성
#   - 1. 생성, 2.호출
# 함수는 생성하면 아무 동작도 안한다.
# 반드시 생성 후 호출을 통해서 사용
def movie_title_crawler(movie_code):
    url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'

    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')

    title = doc.select('h3.h_movie > a')[0].getText()
    return title


# 리뷰 수집(리뷰, 평점, 작성자, 작성일자)
def movie_review_crawler(movie_code):
    title = movie_title_crawler(movie_code)  # 제목 수집
    # 리뷰를 수집하는 코드 작성!
    print(f'>> Start collecting movies for {title}')

    # set {제목, 리뷰, 평점, 작성자, 작성일자}
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
    result = requests.get(url)

    doc = BeautifulSoup(result.text, 'html.parser')
    all_count = doc.select('strong.total > em')[0].get_text()  # 리뷰 전체 count

    # "2,480" : str type(문자열)
    # print(type(all_count))

    # "2480" -> 2480(int로 변환 가능)
    # "2,480" -> 문자포함 변환 안됨. (',' 포함으로 인해)

    # 1. 숫자만 추출: 정규식
    numbers = re.sub(r'[^0-9]', '', all_count)
    pages = math.ceil(int(numbers) / 10)
    print(f'The total number of pages to collect is {pages}')

    # 해당 페이지 리뷰 수집!
    count = 0  # 전체 리뷰 수 count
    for page in range(1, pages + 1):
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'

        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        review_list = doc.select('div.score_result > ul > li')  # 1page의 리뷰 10건

        # review 한 건씩 수집
        for i, one in enumerate(review_list):
            #  리뷰, 평점, 작성자, 작성일자  + 전처리
            score = one.select('div.star_score > em')[0].get_text()
            original_date = one.select('div.score_reple dt > em')[1].get_text()

            review = one.select('div.score_reple > p > span')[-1].get_text().strip()
            # 전처리: 날짜 시간-> 날짜만 추출(시간 제거)
            # 날짜는 항상 16글자로 구성
            date = original_date[:10]  # 문자열 추출
            # 문자열 추출
            # [시작:끝+1], 끝은 포함 x
            # [:15] 0~14
            # [3:] 3~끝까지

            original_writer = one.select('div.score_reple dt > em')[0].get_text().strip()
            idx_end = original_writer.find('(')  # (의 인덱스번호를 찾는다.
            writer = original_writer[:idx_end]

            count += 1
            print(f"## 리뷰_{count} #########################################################")
            print(f'# Date: {date}')
            print(f'# Writer: {writer}')
            print(f'# Review: {review}')
            print(f'# Score: {score}\n')
            # Review data 생성
            # -> 규격(포맷) -> JSON
            # JSON 데이터 주고받을 때 많이 사용하는 타입
            # MongoDB -> BSON (Binary JSON) = JSON
            # python의 dictionary = json
            #
            # python dictionary = JSON = BSON
            # JSON 포맷
            # {key:value, key:value, key:value}

            # dict type은 데이터 꺼낼 때 key 값
            # list type은 데이터 꺼낼 때 index 값
            data = {
                'title': title,
                'score': score,
                'review': review,
                'writer': writer,
                'date': date
            }
            create_review(data)

# 수집(리뷰) -> 저장(db) -> 전처리, 탐색 -> 딥러닝모델 학습 & 평가(긍부정 분석기) -> 시각화 or 실제 데이터 서비스

# MongoDB 데이터베이스
# 1. Local(컴퓨터) 설치
# 2. 웹 클라우드 사용(ip, 내부 ip 사용 x)