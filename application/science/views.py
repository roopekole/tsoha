from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.science.models import Science
from application.science.forms import SciForm

@app.route("/sciences", methods=["GET"])
def scis_index():

    if not current_user.admin:
        return "Access denied"

    return render_template("science/list.html", prevented_scis = Science.sciWithThesis(), scis = Science.query.all())


# Delete science
@app.route("/science/delete/<sci_id>/", methods=["POST"])
@login_required(role="ADMIN")
def sci_delete(sci_id):
   
    sci = Science.query.get(sci_id)
    
    db.session().delete(sci)
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

    sci = Science(form.name.data)
    
    db.session().add(sci)
    db.session().commit()
  
    return redirect(url_for("scis_index"))