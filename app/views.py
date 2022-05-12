# from app import app
from flask import render_template
from flask import url_for
from flask import request


def home():
    return render_template("home.html")


# @app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        return f"result: {result['fname']}"  # render_template("result.html", result=result)


# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello(name=None):
#     return render_template("hello.html", name=name)
#     ##return f"Hello {name}"
