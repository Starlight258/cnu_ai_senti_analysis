import requests
from bs4 import BeautifulSoup

url = 'https://n.news.naver.com/article/660/0000019070?sid=101'
# SSL Error -> requests.get(url, verify=False)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, liek Gecko) Chrome/92.0.4515.131 Safari/537.36'}

result = requests.get(url, headers=headers)
doc = BeautifulSoup(result.text, 'html.parser')
title = doc.select('h2.media_end_head_headline')[0].get_text()

# get_text() : 태그를 제거하고 text만 추출
# strip() : 앞 뒤 공백을 제거(가운데X)
# - 회원가입
content = doc.select('div#dic_area')[0].get_text().strip()

print(f'본문: {title}') #fstring-요즘 제일 많이 씀
print('내용: {}'.format(content)) #format

