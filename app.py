from flask import Flask
from mydecorator import pass_json

app = Flask(__name__)


@app.route("/hello", methods=["POST"])
@pass_json()
def hello(name, family):
    message = f"Hello, {name} {family}!"
    return {"status": 0, "message": message}


@app.route("/seeyou", methods=["POST"])
@pass_json("key1", "key2")
def seeyou(name, family):
    message = f"See you, {name} {family}!"
    return {"status": 0, "message": message}


@app.route("/thankyou", methods=["POST"])
@pass_json(family="key2")
def thankyou(name, family):
    message = f"Thank you, {name} {family}!"
    return {"status": 0, "message": message}
