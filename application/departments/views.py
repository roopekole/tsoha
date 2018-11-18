from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required
from application.departments.models import Dept
from application.departments.forms import DeptForm

@app.route("/departments", methods=["GET"])
def depts_index():
    return render_template("departments/list.html", depts = Dept.query.all())


# Delete department
@app.route("/deparment/delete/<dept_id>/", methods=["POST"])
def dept_delete(dept_id):
   
    d = Dept.query.get(dept_id)
    
    db.session().delete(d)
    db.session().commit()

    return redirect(url_for("depts_index"))

@app.route("/department/new/")
@login_required(role="ADMIN")
def dept_form():
    return render_template("departments/new.html", form = DeptForm())

@app.route("/department/", methods=["POST"])
@login_required(role="ADMIN")
def dept_create():
    form = DeptForm(request.form)
  
    if not form.validate():
        return render_template("department/new.html", form = form)

  
    t = Dept(form.name.data)
    
    print("#############")
    print(t)
    print("#############")
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("depts_index"))