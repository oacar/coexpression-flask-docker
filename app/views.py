from app import app
from flask import render_template
from flask import url_for


@app.route("/")
def home():
    return "<b>Hello world changed</b>"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)
    ##return f"Hello {name}"


@app.route("/template")
def template():
    return render_template("home.html")


with app.test_request_context():
    print(url_for("home"))
    print(url_for("hello"))
    print(url_for("hello", name="omer"))
## print(url_for('profile', username='John Doe'))
