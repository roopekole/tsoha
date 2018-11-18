from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, AccountForm, NewAccountForm

from application.departments.models import Dept

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    

    user = User.query.filter_by(userID=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                                error = "No such username or password")


    login_user(user)
    return redirect(url_for("index"))    

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    


@app.route("/account", methods=["GET"])
def accounts_index():
    return render_template("auth/list.html", users = User.query.outerjoin(Dept, User.department == Dept.departmentID).all())

@app.route("/account/new/")
@login_required(role="ADMIN")
def account_form():
    departments = Dept.query.all()
    form = NewAccountForm()
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
    return render_template("auth/new.html", form = form)

@app.route("/account/<account_id>/", methods=["GET"])
def account_edit(account_id):
    
    user = User.query.get(account_id)
 
    departments = Dept.query.all()
    
    form = AccountForm(username = user.userID, firstname = user.firstName, lastname = user.lastName,
                       admin = user.admin, departments = user.department)
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
        
    return render_template("auth/edit.html", user = user, form = form)

@app.route("/account/edit/<account_id>/", methods=["POST"])
def account_update(account_id):
   
    user = User.query.get(account_id)
    form = AccountForm(request.form)
    user.firstName = form.firstname.data
    user.lastName = form.lastname.data
    user.department = form.departments.data
    user.admin = form.admin.data

    db.session.commit()
    return redirect(url_for("accounts_index"))
    

@app.route("/account/delete/<account_id>/", methods=["POST"])
def user_delete(account_id):
   
    u = User.query.get(account_id)
    
    db.session().delete(u)
    db.session().commit()

    return redirect(url_for("accounts_index"))

@app.route("/account/", methods=["POST"])
@login_required(role="ADMIN")
def account_create():
    form = NewAccountForm(request.form)
  
    #if not form.validate():
       # return render_template("auth/new.html", form = form)
    if form.admin.data == False:
        form.admin.data == False
    else:
        form.admin.data == True
  
    t = User(form.username.data, form.firstname.data, form.lastname.data, form.password.data, form.departments.data, form.admin.data)
    
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("accounts_index"))