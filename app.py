# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Initialize database
# def init_db():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT,
#                     email TEXT UNIQUE,
#                     password TEXT
#                 )''')
#     conn.commit()
#     conn.close()

# @app.route('/')
# def index():
#     #return {"message":"Hello from server"}
#     return render_template('index.html')

# @app.route('/signup', methods=['POST'])
# def signup():
#     name = request.form['name']
#     email = request.form['email']
#     password = request.form['password']

#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     try:
#         c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('index', show_login='true'))  # Redirect with query param to open login modal
#     except sqlite3.IntegrityError:
#         conn.close()
#         return "Email already registered. Try logging in."

# # if __name__ == '__main__':
# #     init_db()
# #     app.run(debug=True)
