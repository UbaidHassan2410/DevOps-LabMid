from flask import Flask, render_template, request, redirect, flash
from urllib.parse import urlparse
import sqlite3, os
app = Flask(__name__)
app.secret_key = 'lab-demo-key'
DB = os.environ.get('SUBMISSIONS_DB', 'submissions.db')

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY, name TEXT NOT NULL, registration TEXT NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL)')

def valid_url(url):
    try:
        p = urlparse(url)
        return p.scheme in ('http','https') and bool(p.netloc) and bool(p.hostname) and '.' in p.hostname
    except (ValueError, TypeError):
        return False

@app.route('/', methods=['GET','POST'])
def index():
    init_db()
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        registration = request.form.get('registration','').strip()
        title = request.form.get('title','').strip()
        url = request.form.get('url','').strip()
        if not all([name, registration, title, url]):
            flash('All fields are required, including registration number.', 'error')
        elif not valid_url(url):
            flash('Invalid submission URL. Use http:// or https://.', 'error')
        else:
            with sqlite3.connect(DB) as conn:
                conn.execute('INSERT INTO submissions (name,registration,title,url) VALUES (?,?,?,?)',(name,registration,title,url))
            flash('Submission saved successfully.', 'success')
            return redirect('/')
    with sqlite3.connect(DB) as conn:
        rows = conn.execute('SELECT name,registration,title,url FROM submissions ORDER BY id DESC').fetchall()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
