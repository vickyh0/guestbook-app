import os
from contextlib import closing
import psycopg2
from flask import Flask, request, redirect, render_template_string, jsonify

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"], dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"],
        connect_timeout=3,
    )

def init_db():
    with closing(get_conn()) as conn, conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY, name TEXT NOT NULL,
            body TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT now())""")
        conn.commit()

PAGE = """
<h1>Guestbook</h1>
<form method="post" action="/sign">
  <input name="name" placeholder="Name" required maxlength="50">
  <input name="body" placeholder="Message" required maxlength="200">
  <button>Sign</button>
</form>
<ul>{% for n, b, t in rows %}<li><b>{{ n }}</b>: {{ b }} <small>{{ t }}</small></li>{% endfor %}</ul>
"""

@app.get("/")
def index():
    with closing(get_conn()) as conn, conn.cursor() as cur:
        cur.execute("SELECT name, body, created_at FROM messages ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
    return render_template_string(PAGE, rows=rows)

@app.post("/sign")
def sign():
    with closing(get_conn()) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO messages (name, body) VALUES (%s, %s)",
                    (request.form["name"][:50], request.form["body"][:200]))
        conn.commit()
    return redirect("/")

@app.get("/health")
def health():
    try:
        with closing(get_conn()) as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        return jsonify(app="ok", database="ok"), 200
    except Exception as e:
        return jsonify(app="ok", database="down"), 503

init_db()