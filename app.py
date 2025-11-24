from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# init db
def init_db():
    with sqlite3.connect("notes.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS notes
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      content TEXT NOT NULL,
                      timestamp TEXT)""")
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("note")
        if content.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with sqlite3.connect("notes.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO notes (content, timestamp) VALUES (?, ?)",
                          (content, timestamp))
                conn.commit()
        return redirect(url_for("index"))

    # load notes
    with sqlite3.connect("notes.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM notes ORDER BY id DESC")
        notes = c.fetchall()

    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>")
def delete(note_id):
    with sqlite3.connect("notes.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)