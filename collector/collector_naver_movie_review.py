import math

import requests
from bs4 import BeautifulSoup
import re
import math

##################
# 1. 영화 제목 수집 #
##################

# movie_code : 네이버 영화 코드(6자리 숫자)

# 제목 수집
# 함수
#  - 1.생성, 2.호출
#  - 함수는 생성하면 아무 동작 X
#  - 반드시 생성 후 호출을 통해서 사용!


def movie_title_crawler(movie_code):
    url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    title = doc.select('h3.h_movie > a')[0].get_text()  # 자식인 a태그
    return title


# 리뷰 수집(리뷰, 평점, 작성자, 작성일자) + 제목
def movie_review_crawler(movie_code):
    title = movie_title_crawler(movie_code) # 제목 수집
    print(f'>>Start collecting movies for {title}')
    
    # set {제목, 리뷰, 평점, 작성자, 작성 일자}
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    all_count = doc.select('strong.total > em')[0].get_text()  # 리뷰 전체 수
    # "2,480" : str type(문자열)
    # ex) 문자열 / 10 (X)
    # int type(정수형 숫자)
    # print(type(all_count))
    # "2480" -> 2480 (O)
    # "2,480" -> 문자 포함 변환(X)

    # 1. 숫자만 추출 : 정규식
    numbers = re.sub(r'[^0-9]', '', all_count)  # 0-9까지를 제외하고 다 ''으로 취급
    pages = math.ceil(int(numbers)/10)  # 올림 ceil()
    print(f'The total number of pages to collect is {pages}')
    # 2480건 / 10
    # 해당 페이지 리뷰 수집!
    count = 0  # 전체 리뷰수를 count
    for page in range(1, pages+1):  # 전체 페이지 리뷰 수집
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        review_list = doc.select(('div.score_result > ul > li'))
        for i, one in enumerate(review_list):
            # 리뷰, 평점, 작성자, 작성 일자
            score = one.select('div.star_score > em')[0].get_text()
            review = one.select('div.score_reple > p > span')[-1].get_text().strip() #마지막 값 가져오기
            print(f'# Review: {review}')
            print(f'# Score: {score}')
            break;
    return review_list

