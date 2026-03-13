# Algoritme som bruker salt & pepper X
# Krypteringsfunksjon X

# TODO: Lagring av brukerdata - Ser på det imorgen

from flask import Flask, render_template, request, redirect, session
from src.decorators import login_required
from werkzeug.exceptions import HTTPException
from src.user import User, get_all, get, add_note, get_notes_by_user
from pprint import pprint

# Temporary (RAM lagring)
users = get_all()  # Type {str, User}

app = Flask(__name__)
app.secret_key = "3hfdsajfhskruk"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/log-out")
def log_out():
    session.clear()
    return redirect("/")


@app.route("/register")
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    fornavn = request.form.get("fornavn", "").strip()
    etternavn = request.form.get("etternavn", "").strip()

    if not username or not password or not fornavn or not etternavn:
        return render_template(
            "register.html",
            error_msg="Alle felt må fylles ut.",
            form=request.form
        )

    if username in users or get(username):
        return render_template(
            "register.html",
            error_msg="Brukernavnet finnes allerede.",
            form=request.form
        )

    user = User(
        username=username,
        password=password,
        fornavn=fornavn,
        etternavn=etternavn
    )

    users[user.username.lower()] = user
    session["user"] = user.username
    session["logged_in"] = True
    pprint(users)
    return redirect("/min-profil")


@app.route("/min-profil")
@login_required
def min_profil():
    username = session.get("user")
    bruker = get(username)

    if not bruker:
        session.clear()
        return redirect("/log-in")

    notes = get_notes_by_user(username)
    return render_template("min_profil.html", bruker=bruker, notes=notes)


@app.route("/log-in")
def get_login():
    return render_template("login.html")


@app.route("/log-in", methods=["POST"])
def post_login():
    username = request.form.get("username", "").lower().strip()
    password = request.form.get("password", "")

    user = users.get(username, False)

    if not user:
        user = get(username)

    if not user or not user.check_password(password):
        return render_template(
            "login.html",
            error_msg="Feil brukernavn eller passord.",
            form=request.form
        )

    users[user.username.lower()] = user
    session["user"] = user.username
    session["logged_in"] = True
    return redirect("/min-profil")


@app.route("/add-note", methods=["POST"])
@login_required
def add_note_route():
    username = session.get("user")
    content = request.form.get("content", "").strip()

    if content:
        add_note(username, content)

    return redirect("/min-profil")


@app.route("/comment/<post_id>", methods=["GET"])
def comment(post_id):
    form_data = request.form
    comment = form_data.get("comment")
    if not session.get("logged_in"):
        return "du må logge inn :("
    return "OK"


# Dev mode:
if __name__ == "__main__":
    app.run(debug=True)