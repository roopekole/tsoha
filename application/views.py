from flask import render_template, session
from application import app
from application.auth.models import User

@app.route("/")
def index():
    return render_template("index.html")

# Pass inactive users to the management badge
# This is currently causing trouble in heroku and not yet fully functional locally either
app.jinja_env.globals.update(inactive_users=User.countInactives())