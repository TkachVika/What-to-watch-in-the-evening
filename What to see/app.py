from flask import Flask, render_template, request, jsonify
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret123"

from movies import movies

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    if "user" not in session:
        return jsonify({"redirect": "/login"}), 401

    title = request.json.get("title")

    if "favorites" not in session:
        session["favorites"] = []

    if title not in session["favorites"]:
        session["favorites"].append(title)

    session.modified = True
    return jsonify({"ok": True})


@app.route("/favorites")
def favorites():
    if "user" not in session:
        return redirect("/login")

    fav_titles = session.get("favorites", [])
    fav_movies = [m for m in movies if m["title"] in fav_titles]

    return render_template("favorites.html", movies=fav_movies)



# 🔍 AJAX-пошук
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()

    filtered = [
        m for m in movies
        if query in m["title"].lower()
    ]

    return jsonify(filtered)


# 🏠 Головна сторінка
@app.route("/", methods=["GET", "POST"])
def index():
    result = []

    if request.method == "POST":

        user_type = request.form.get("type")
        genre = request.form.get("genre")
        user_time = int(request.form.get("time"))

        for m in movies:
            if m["type"] != user_type:
                continue
            if genre not in m["genre"]:
                continue
            if m["time"] > user_time:
                continue


            result.append(m)

    return render_template("index.html", result=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        avatar = request.form["avatar"]

        # зберігаємо користувача
        session["user"] = {
            "username": username,
            "avatar": avatar
        }
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
