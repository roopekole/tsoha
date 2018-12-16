from flask import render_template, session
from application import app
from application.auth.models import User

@app.route("/")
def index():
    return render_template("index.html")

