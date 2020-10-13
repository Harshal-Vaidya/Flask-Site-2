from flask import Flask, flash, redirect, render_template, request, session, abort
import mysql.connector

import os

app = Flask(__name__)
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="eqax")

app.config['SECRET_KEY'] = os.urandom(12)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/resources')
def results():
    return render_template('results.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('Login.html')


@app.route('/logged', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        cursor = mydb.cursor()
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        cursor.execute("SELECT * FROM USERS WHERE EMAIL = '"+email+"' AND  PASSWORD  ='"+password+"'")
        rows = cursor.fetchall()
        count = len(rows)
        if count == 1:
            session['user'] = email
            return render_template('users.html',email=email)
        else:
            return render_template('not sample.html')
        cursor.close()


@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('inputUsername')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        cursor = mydb.cursor()
        cursor.execute(''' INSERT INTO users(username,email,password) VALUES(%s,%s,%s)''', (user_name, email, password))
        mydb.commit()
        cursor.close()
        return render_template('sample.html', user_name=user_name)


app.run(debug=True)
