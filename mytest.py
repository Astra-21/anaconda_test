from flask import Flask, render_template
import mysql.connector
#reder_template:　括弧の中身から引っ張ってくる機能

app = Flask(__name__)#インスタンス化

#mysql接続
db = mysql.connector.connect(
    host="localhost",        # MySQLのホスト名（通常は "localhost"）
    user="root",        # 作成したMySQLユーザー名（デフォルトなら "root"）
    password="Twoce22Hall",  # 設定したパスワード
    database="example"       # 作成したデータベース名
)
@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT shohin_id, shohin_mei FROM shohin")  # `users` テーブルのデータを取得
    records = cursor.fetchall()
    cursor.close()
    return render_template("index.html", records=records)




@app.route("/admin")#webアノテーションみたいな
def hello_world():#関数名

    #動的なwebページの作成
    #本来はデータベースから値を取得してhtmlに埋め込む
    radioes = {
        'title1': 'オードリー',
        'title2': 'マユリカ',
        'title3': 'カベポスター'
    },{
        'title1':'ワンピーす',
        'title2': 'ナルト',
        'title3': '進撃の巨人'
    }

    sports = {
        'title1': 'アーセナル',
        'title2': 'リヴァプール',
        'title3': 'フラム'
    },{
        'title1':'アビスパ福岡',
        'title2': '川崎フロンターレ',
        'title3': '名古屋グランパス'
    }
    
    return render_template("admin.html",radioes= radioes)

    #if numbers==1:
    #   return render_template("admin.html",radioes= radioes)
    #elif  numbers==2:
    #    return render_template("admin.html",radioes= sports)
    
    