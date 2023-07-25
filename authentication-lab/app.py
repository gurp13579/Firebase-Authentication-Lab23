from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {"apiKey": "AIzaSyA-SwDspYYOM3R3peaUlKuM293G3jrBsVk",
  "authDomain": "fir-authentication-5d473.firebaseapp.com",
  "projectId": "fir-authentication-5d473",
  "storageBucket": "fir-authentication-5d473.appspot.com",
  "messagingSenderId": "252152093008",
  "appId": "1:252152093008:web:4a5421e37a6fe70e2bb455",
  "databaseURL": "https://fir-authentication-5d473-default-rtdb.europe-west1.firebasedatabase.app/"
}



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    else:
        try:
            request.method == "POST"
            email = request.form['email']
            password = request.form['password']
            login_session['user']['localId'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            print("password or email is wrong")
            return render_template('signin.html')
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        request.method == "POST"
        email = request.form['email']
        password = request.form['password']
        try:
            UID = login_session['user']['localId'] = auth.create_user_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            print("email already exists")
            return render_template('signup.html')
    

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'GET':
        return render_template('add_tweet.html')
    else:
        tweet = {'title':request.form['title'],'text':request.form['text']}
        db.child('Tweets').push(tweet)
        return redirect(url_for("show_tweet"))

@app.route('/all_tweets', methods=['GET','POST'])
def show_tweet():
    return render_template('tweets.html', d = db.child("Tweets").get().val())

if __name__ == '__main__':
    app.run(debug=True)

