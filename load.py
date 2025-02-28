from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid  # ユニークIDを生成するためのモジュール
import os
#import pytz
from datetime import datetime

app = Flask(__name__)

# MySQLの接続設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Twoce22Hall@localhost/example' #flaskのアプリの中に設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #?

db = SQLAlchemy() #SQLをインスタンス化したらそのメソッドには何が使えるようになったのだろう？
db.init_app(app) #initが初期化なのはわかる、_appガついていいんか？de.init(app)じゃだめなの？
migrate = Migrate(app, db) 

# Blogモデル、この段階ではまだテーブル作られてない,定義
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True) #列のことをcolumnsという
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)#utcnowに下線ひかれてるけど何？(chatこの括弧内は無視して2:07)
    #Hyogo_timeZone = pytz.timezone('Asia/Tokyo') ''で囲んだり""だ囲んだりそのルールみたいなのはあるの？ youtubeではpytzと書いてあったがこれは何がしたいの？
    image_name = db.Column(db.String(100), nullable=True)

# Userモデル
#class Personal(db.Model):#後に作る

@app.route("/")    
def index():
    blogs = Blog.query.all()
    return render_template("index.html", records=blogs)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        unique_id = uuid.uuid4().int % (2**31 - 1)
        image = request.files["image"]
        imagename = image.filename

        if not (imagename.endswith(".jpg") or imagename.endswith(".png")):
            return redirect("/admin")

        save_path = os.path.join(app.static_folder, 'img', imagename)
        image.save(save_path)

        new_blog = Blog(id=unique_id, title=title, body=body, image_name=imagename)
        db.session.add(new_blog)
        db.session.commit()

        return redirect("/admin")

    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
