from flask import Flask, render_template, request, redirect
import mysql.connector
import uuid  # ユニークIDを生成するためのモジュール
from flask_migrate import Migrate
import os

app= Flask(__name__)

db = mysql.connector.connect(
    host="localhost",        # MySQLのホスト名（通常は "localhost"）
    user="root",        # 作成したMySQLユーザー名（デフォルトなら "root"）
    password="Twoce22Hall",  # 設定したパスワード
    database="example"       # 作成したデータベース名
)
@app.route("/")
def index():
    #動的なwebページの作成
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT*FROM blog")
    records = cursor.fetchall()
    cursor.close()
    
    return render_template("index.html",records = records)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        title = request.form.get("title")
        body = request.form.get("body")
        unique_id = uuid.uuid4().int % (2**31 - 1)
        image = request.files['image']#画像データそのものを取得してる、左辺はファイルオブジェクト
        imagename= image.filename

        if not(imagename.endswith(".jpg") or imagename.endswith(".png")):
            return redirect("/admin")
        
        save_path = os.path.join(app.static_folder,'img', imagename) #staticではなくてstatc_folderなん？=>ok
        image.save(save_path)#imageをsave_pathに保存
        cursor = db.cursor() #MySQLデータベース (db) とのやり取りをするためのカーソル（cursor）オブジェクト を作成
        
        sql = "INSERT INTO blog (id, title, body, image) VALUES (%s, %s, %s, %s)"
        values = (unique_id, title, body, imagename)
        cursor.execute(sql, values)
        db.commit()  # データベースへ変更を反映
        cursor.close()

        return redirect("/admin")


    elif request.method=="GET":
        return render_template("create.html")



@app.route("/admin")#webアノテーションみたいな
def admin():#関数名

    #動的なwebページの作成
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT*FROM blog")
    records = cursor.fetchall()
    cursor.close()
    
    return render_template("admin.html",records = records)

    # user.py
if __name__ == "__main__":
    app.run(debug=True)



@app.route("/<int:number>/update", methods=["GET", "POST"])
def update(number):

    if request.method == "POST":

        cursor = db.cursor(dictionary=True) #MySQLデータベース (db) とのやり取りをするためのカーソル（cursor）オブジェクト を作成
        sql_update = "UPDATE blog SET title = %s, body = %s WHERE id = %s;"
        values = (request.form.get("update_title"), request.form.get("update_body"), number)
        cursor.execute(sql_update, values)
        db.commit()
        cursor.close()  

        return redirect("/admin")


    elif request.method == "GET":
        return render_template("update.html")

@app.route("/<int:number>/delete")
def delete(number):

    cursor = db.cursor(dictionary=True) #MySQLデータベース (db) とのやり取りをするためのカーソル（cursor）オブジェクト を作成
    
    sql_delete = "DELETE FROM blog WHERE id = %s;"
    values = (number, ) #executeはtタプル（要素の中身変更不可）、リストしか使えない
    cursor.execute(sql_delete, values)
    
    db.commit()
    cursor.close()  

    return redirect("/admin")

@app.route("/<int:number>/readMore")
def readMore(number):
    #動的なwebページの作成
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT*FROM blog")
    records = cursor.fetchall()
    cursor.close()
    
    return render_template("readMore.html",records = records)

    