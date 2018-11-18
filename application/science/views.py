from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required
from application.science.models import Science
from application.science.forms import SciForm

@app.route("/sciences", methods=["GET"])
def scis_index():
    return render_template("science/list.html", scis = Science.query.all())


# Delete science
@app.route("/science/delete/<sci_id>/", methods=["POST"])
def sci_delete(sci_id):
   
    d = Science.query.get(sci_id)
    
    db.session().delete(d)
    db.session().commit()

    return redirect(url_for("scis_index"))

@app.route("/science/new/")
@login_required(role="ADMIN")
def sci_form():
    return render_template("science/new.html", form = SciForm())

@app.route("/science/", methods=["POST"])
@login_required(role="ADMIN")
def sci_create():
    form = SciForm(request.form)
  
    if not form.validate():
        return render_template("science/new.html", form = form)

    t = Science(form.name.data)
    
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("scis_index"))