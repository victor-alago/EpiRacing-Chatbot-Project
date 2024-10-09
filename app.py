from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
from chat import get_response
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('epiracing.db')
    conn.row_factory = sqlite3.Row 
    return conn

# Create users table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            year_of_admission INTEGER,
            course_of_study TEXT,
            motivation TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Flask-Login User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_record = cursor.fetchone()
    conn.close()
    if user_record:
        return User(user_record['id'])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address!')
            return redirect(url_for('register'))

        # Password match validation
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Check if email already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists. Please log in.')
            conn.close()
            return redirect(url_for('login'))

        # Save new user to the database
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_record = cursor.fetchone()
        conn.close()

        # Validate credentials
        if user_record and check_password_hash(user_record['password'], password):
            user = User(id=user_record['id'])
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid credentials!')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Process profile form and update the user's details
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        year_of_admission = request.form['year_of_admission']
        course_of_study = request.form['course_of_study']
        motivation = request.form['motivation']

        cursor.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, age = ?, year_of_admission = ?, course_of_study = ?, motivation = ?
            WHERE id = ?
        ''', (first_name, last_name, age, year_of_admission, course_of_study, motivation, current_user.id))

        conn.commit()
        flash('Your profile has been updated successfully!')

    # Fetch the user's profile data
    cursor.execute('SELECT * FROM users WHERE id = ?', (current_user.id,))
    profile_data = cursor.fetchone()
    conn.close()

    return render_template('profile.html', email=profile_data['email'], profile_data=profile_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.get('/')
def index():
    return render_template('base.jinja')


# API endpoint for Chatbot
@app.post('/predict')
def predict():
    if not current_user.is_authenticated:
        return jsonify({"answer": "Hi, to access my full potential, kindly log in or register."})

    text = request.get_json().get('message')
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == '__main__':
    app.run()