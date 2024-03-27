import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[name="description"]')

    title = og_title['content'].split('(')[0].strip()
    image = og_image['content']
    desc = og_description['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive
    }

    db.film.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.film.find({}, {'_id': False}))
    print(movie_list)
    return jsonify({'movies': movie_list})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)