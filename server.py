import os
import flask
import sqlite3
import util

app = flask.Flask(__name__)
app.secret_key = "asds"
util.create_tables()


@app.route("/")
def index_page():
    return flask.render_template("index.html")


@app.route("/signup")
def signup_page():
    return flask.render_template("signup.html")


@app.route("/login")
def login_page():
    return flask.render_template("login.html")


@app.route("/wallet")
def wallet_page():
    return flask.render_template("wallet.html")


@app.route("/register-user", methods=["POST"])
def register_user():
    data = flask.request.json
    ok = True
    try:
        util.register_user(data)
    except Exception as e:
        print(e)
        ok = False
    print(data)
    return flask.jsonify({"ok": ok})


@app.route("/login-user", methods=["POST"])
def login_user():
    data = flask.request.json
    ok = True
    try:
        user = util.login_user(data)
        print(user)
        flask.session['user'] = user[3]
    except Exception as e:
        print(e)
        ok = False
    print(data)
    return flask.jsonify({"ok": ok})


@app.route("/logout", methods=["POST"])
def logout():
    flask.session.pop('user', None)
    return flask.jsonify({"ok": True})


@app.route("/user", methods=["POST"])
def user():
    ok = True
    try:
        email = flask.session["user"]
        user = util.get_user_by_email(email)
        return flask.jsonify({"ok": ok, "data": user})
    except Exception as e:
        ok = False
        print(e)
        return flask.jsonify({"ok": ok, "data": None})


@app.route("/send-btc", methods=["POST"])
def send_btc():
    ok = True
    data = flask.request.json
    tx_hash = None
    try:
        email = flask.session["user"]
        user = util.get_user_by_email(email)
        tx_hash = util.send_btc(wallet_id=user["wallet_id"],
                                amount=data["amount"],
                                receiver_address=data["receiver_address"])
    except Exception as e:
        print(e)
        ok = False
    print(data)
    return flask.jsonify({"ok": ok, "data": tx_hash})


if os.name == "nt":
    app.run(host="0.0.0.0", port="4343", debug=True)
