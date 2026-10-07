import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rmirror_secret_key"

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    platform TEXT
)
""")

conn.commit()

@app.route("/")
def home():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    print("Movies Table =", cursor.fetchall())

    cursor.execute("""
    SELECT movies.*
    FROM movies
    JOIN watch_history
    ON movies.id = watch_history.movie_id
    WHERE watch_history.email=?
    """, (session.get("email"),))
    

    continue_movies = cursor.fetchall()

    print("Continue Movies =", continue_movies)

    return render_template(
        "index.html",
        username=session.get("username"),
        email=session.get("email"),
        movies=movies,
        continue_movies=continue_movies
    )

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if session.get("role") != "admin":
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]
        platform = request.form["platform"]

        cursor.execute(
            "INSERT INTO movies(name, platform) VALUES (Biker, Netflix)",
            (title, platform)
        )

        conn.commit()

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    return render_template("admin.html", movies=movies)


from flask import redirect, url_for

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Admin Login
        if email == "admin@rmirror.com" and password == "admin123":
            session["username"] = "Administrator"
            session["email"] = email
            session["role"] = "admin"

            return redirect(url_for("admin"))

        # User Login
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            session["username"] = user[1]
            session["email"] = user[2]
            session["role"] = "user"

            return redirect(url_for("home"))

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/delete_movie/<int:id>")
def delete_movie(id):

    if session.get("role") != "admin":
        return "Access Denied"

    cursor.execute(
        "DELETE FROM movies WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect(url_for("admin"))

cursor.execute("""
CREATE TABLE IF NOT EXISTS watch_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    movie_id INTEGER,
    progress INTEGER
)
""")

conn.commit()

@app.route("/watch/<int:movie_id>")
def watch(movie_id):

    email = session.get("email")

    cursor.execute(
        "SELECT * FROM watch_history WHERE email=? AND movie_id=?",
        (email, movie_id)
    )

    existing = cursor.fetchone()

    if not existing:
        cursor.execute(
            "INSERT INTO watch_history(email, movie_id, progress) VALUES (?, ?, ?)",
            (email, movie_id, 10)
        )
        conn.commit()

    return render_template("watch.html")

cursor.execute("SELECT * FROM watch_history")
print(cursor.fetchall())


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)