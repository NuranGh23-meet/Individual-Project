from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
"apiKey": "AIzaSyC83wOgNX5JflThhTDTT2F6WmY8sWqMPP0",
"authDomain": "individual-cs-project.firebaseapp.com",
"databaseURL": "https://individual-cs-project-default-rtdb.europe-west1.firebasedatabase.app",
"projectId": "individual-cs-project",
"storageBucket": "individual-cs-project.appspot.com",
"messagingSenderId": "17835995206",
"appId": "1:17835995206:web:3e959e9ecf3e5768b49a47",
"measurementId": "G-J6NW4LJK95",
"databaseURL": "https://individual-cs-project-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask (__name__, template_folder = 'templates', static_folder = 'static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    # return render_template("signin.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try: 
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except: 
            error = "Authentication failed"
    return render_template("signin.html", error = error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error=""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
        #return render_template(home.html) 

		try: 
			login_session['user'] = auth.create_user_with_email_and_password(email , password)
			user = {'username' : request.form['username'] , 'full_name': request.form['full_name'], 'email': request.form['email'],'password': request.form['password']}
			db.child("users").child(login_session['user']['localId']).set(user)
			return render_template('home.html')

		except: 
			error = "Authentication failed"
	return render_template("signup.html", error = error)


@app.route('/home', methods=['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template("about.html")


@app.route('/quizzes', methods=['GET','POST'])
def quizzes():
    if request.method == "POST":
        points = 0
        answer1 = request.form['question1']
        if answer1 == "shut his ears in the oven door":
            points += 1
        answer2 = request.form['question2']
        if answer2 == "barmy old codger":
            points += 1
        answer3 = request.form['question3']
        if answer3 == "a sock":
            points += 1
        answer4 = request.form['question4']
        if answer4 == "wheezy":
            points += 1
        answer5 = request.form['question5']
        if answer5 == "bad dark wizard":
            points += 1

    return render_template ("quizzes.html")


@app.route('/news', methods=['GET','POST'])
def news():
    return render_template ("news.html")

@app.route('/final', methods=['GET','POST'])
def final():
    return render_template ("final.html")


	# return render_template("home.html")
    # try:
    #     home = {"title":request.form['title'], "text":request.form ['text'], 'uid':login_session['user']['localId']}
    #     #db.child("home").push(home)
    #     return render_template("quizzes.html")
    # except:
    #     print('error')
    #     return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
