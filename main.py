from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cbc' 

users = {}  

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if username in users:
            return 'User already exists!'
        users[username] = {'password': password, 'info': {}}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    
    return render_template('login.html')

@app.route('/home')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/add-info', methods=['GET', 'POST'])
def add_info():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    username = session['username']
    user = users[username]
    submitted_data = user['info']

    if request.method == 'POST':
        user['info'] = {
            'fname': request.form['fname'],
            'mname': request.form['mname'],
            'lname': request.form['lname'],
            'age': request.form['age'],
            'address': request.form['address'],
            'birthday': request.form['birthday']
        }

    return render_template('add_info.html', data=submitted_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


