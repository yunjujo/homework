from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    lyrics_receive = request.form['lyrics_give']
    # 2. meta tag를 스크래핑하기
    # URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, tr들을 불러오기
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    doc = {
        'title' : title,
        'image' : image,
        'desc' : lyrics_receive,
        'url' : url_receive,
        'comment' : comment_receive,
        'like' : 0
    }
    db.music.insert_one(doc)

    # 3. mongoDB에 데이터 넣기
    return jsonify({'result': 'success', 'msg': '저장이 완료되었습니다!'})


@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    musics = list(db.music.find({}, {'_id': False}).sort('like', -1))
    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'musics': musics})

@app.route('/memo/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 title_give를 title_receive 변수에 넣습니다.
    title_receive = request.form['title_give']

    # 2. music 목록에서 find_one으로 title이 title_receive와 일치하는 star를 찾습니다.
    music_title = db.music.find_one({'title' : title_receive})

    # 3. music_title의 like 에 1을 더해준 music_like 변수를 만듭니다.
    new_like = music_title['like'] + 1

    # 4. music 목록에서 title이 title_receive인 문서의 like 를 new_like로 변경합니다.
    db.music.update_one({'title' : title_receive}, {'$set':{'like':new_like}})
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)