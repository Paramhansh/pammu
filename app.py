from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a SQLite database and a submissions table for storing contact form data.
conn = sqlite3.connect('contact.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = sqlite3.connect('contact.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('thankyou'))

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/submissions')
def submissions():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions")
    submissions = cursor.fetchall()
    conn.close()

    return render_template('submissions.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
