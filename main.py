from flask import Flask, render_template, request, redirect, session
import mysql.connector as connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
con = connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='vishav2002',
    database='login_db')
cur = con.cursor()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/form_validation', methods=['POST'])
def form_validation():
    name = request.form.get('name')
    password = request.form.get('pwd')

    cur.execute("SELECT * FROM user WHERE u_name='{}' AND u_pwd='{}'".format(name, password))
    users = cur.fetchall()
    # users is a list of tuples containing u_name and u_pwd
    if len(users) > 0:
        session['user_id'] = users[0][2]
        return redirect('/home')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upwd')

    cur.execute("INSERT INTO user(u_name,u_pwd,u_id) VALUES ('{}','{}',UUID())".format(
        name, password))
    con.commit()
    cur.execute("select * from user where u_name='{}' and u_pwd='{}'".format(name, password))
    newuser=cur.fetchall()
    session['user_id']=newuser[0][2]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


# main driver function
if __name__ == '__main__':
    app.run(debug=True)
