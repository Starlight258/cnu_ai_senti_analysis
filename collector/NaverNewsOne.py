import requests
from bs4 import BeautifulSoup

url = 'https://n.news.naver.com/article/660/0000019070?sid=101'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, liek Gecko) Chrome/92.0.4515.131 Safari/537.36'}
result = requests.get(url, headers=headers)
doc = BeautifulSoup(result.text, 'html.parser')
title = doc.select('h2.media_end_head_headline')[0].get_text()
print(title)
