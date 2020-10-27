import requests
from bs4 import BeautifulSoup

url = 'http://jamlab.kr/221795308869'

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
title = soup.select_one('head > title').text
image = soup.select_one('meta[property="og:image"]')['content']
desc = soup.select_one('#d_video_summary > div').text

print(title, image, desc)
