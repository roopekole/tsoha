from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.theses.models import Thesis
from application.theses.forms import ThesisForm


@app.route("/theses", methods=["GET"])
def theses_index():
    return render_template("theses/list.html", theses = Thesis.query.all())

@app.route("/theses/new/")
@login_required
def theses_form():
    return render_template("theses/new.html", form = ThesisForm())

  
@app.route("/theses/<thesis_id>/", methods=["POST"])
def theses_set_done(thesis_id):

    t = Thesis.query.get(thesis_id)
    t.done = True
    db.session().commit()
  
    return redirect(url_for("theses_index"))

@app.route("/theses/", methods=["POST"])
def theses_create():
    form = ThesisForm(request.form)

    if not form.validate():
        return render_template("theses/new.html", form = form)


    t = Thesis(form.title.data, form.description.data, current_user.UserID)
        
    db.session().add(t)
    db.session().commit()
    
    return redirect(url_for("theses_index"))