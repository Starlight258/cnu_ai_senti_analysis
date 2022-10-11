#주석!!
# -> 개발자의 메모장!!
# -> 파이썬이 주석은 실행 X

#파이썬의 경로
#1.프로젝트(cnu_ai_senti_analysis-main)
# 2.python package(collector)
#  3.Python file(test.py, DaumNewsOne.py)
# - python package: python file들을 모아두는 폴더
#                   폴더 아이콘 안에 구멍 뚫려있음

#import와 Library(module)
#- 파이썬 코드를 직접 작성해서 개발할수도 있지만
# -다른 개발자가 이미 만들어놓은 코드를 사용하면 편리함
# -이미 개발되어있는 코드들의 욲음 = 라이브러리(module)
#   1.built in Library: Python 설치하면 자동으로 제공
#                       예: math, sys, os 등
#   2.외부 Library: 여러분이 직접 추가해서 사용!
#                    예:request,beautiflusoup4 등

# Library를 사용하기위해서는 import 작업 진행
# - import는 도서관에서 필요한 책을 빌려오는 개념

import requests # 책 전체를 빌려옴
from bs4 import BeautifulSoup # bs4라는 책에서 BeautifulSoup 1개 파트만 빌려옴

# 목표: Daum 뉴스 웹페이지의 제목과 본문 데이터를 수집!
#   1.url: https://v.daum.net/v/20221006103847242
#   2.requests로 해당 url의 html 전체 코드를 수집!

url = 'https://v.daum.net/v/20221006103847242'
result = requests.get(url)
# print(result.text)
# 3.beautifulsoup을 통해서 '제목과 본문'만 추출
doc = BeautifulSoup(result.text, 'html.parser')
# python은 []: List Type
# index0  1  2  3    4
#   - [5, 6, 9, 10, 15] : List 내에는 다양한 데이터 저장 가능
title = doc.select('h3.tit_view')[0].get_text()

print(f'뉴스제목: {title}')
