from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from passlib.hash import sha256_crypt
from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, AccountForm, NewAccountForm

from application.departments.models import Dept
from application.theses.models import Thesis

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        # Set the previous page into memory
        session['url'] = request.referrer
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    

    user = User.query.filter_by(userID=form.username.data).first()
    # Return with error if no user
    if not user:
        return render_template("auth/loginform.html", form = form,
                                error = "No such username or password")
    # Also return if no password match
    if not(sha256_crypt.verify(form.password.data, user.password)):
        return render_template("auth/loginform.html", form = form,
                                error = "No such username or password")
    
    login_user(user)
    # get the previous page from memory
    if 'url' in session:
        return redirect(session['url'])
         
    return redirect(url_for("index"))    

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    


@app.route("/account", methods=["GET"])
def accounts_index():
    users =  User.query.outerjoin(Dept, User.department == Dept.departmentID).all()
    theses_users = Thesis.query.distinct(Thesis.userID)
    theses_users = [user.userID for user in theses_users]
    return render_template("auth/list.html", theses_users = theses_users, users = users)

@app.route("/account/new/")
@login_required(role="ADMIN")
def account_form():
    if not current_user.admin:
        return "Access denied"
    departments = Dept.query.all()
    form = NewAccountForm()
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
    return render_template("auth/new.html", form = form)

@app.route("/account/<account_id>/", methods=["GET"])
@login_required(role="ADMIN")
def account_edit(account_id):
    if not current_user.admin:
        return "Access denied"
    user = User.query.get(account_id)
    
    departments = Dept.query.all()
    
    form = AccountForm(username = user.userID, firstname = user.firstName, lastname = user.lastName,
                       admin = user.admin, 
                       departments = user.department)
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
        
    return render_template("auth/edit.html", user = user, form = form)

@app.route("/account/edit/<account_id>/", methods=["POST"])
def account_update(account_id):
    if not current_user.admin:
        return "Access denied"
    user = User.query.get(account_id)
    form = AccountForm(request.form)

    departments = Dept.query.all()
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
    # This is needed to validate the form correctly
    value = dict(form.departments.choices).get(form.departments.data)

    if not form.validate():
        return render_template("auth/edit.html", user = user, form = form)
    user.firstName = form.firstname.data
    user.lastName = form.lastname.data
    user.department = form.departments.data
    if form.admin.data == False:
        user.admin = 0
    else:
        user.admin = 1

    db.session.commit()
    return redirect(url_for("accounts_index"))
    

@app.route("/account/delete/<account_id>/", methods=["POST"])
def user_delete(account_id):
    if not current_user.admin:
        return "Access denied"
    u = User.query.get(account_id)
    
    db.session().delete(u)
    db.session().commit()

    return redirect(url_for("accounts_index"))

@app.route("/account/", methods=["POST"])
@login_required(role="ADMIN")
def account_create():
    form = NewAccountForm(request.form)
  
    departments = Dept.query.all()
    form.departments.choices = [(department.departmentID, department.name) for department in departments]
    # This is needed to validate the form correctly
    value = dict(form.departments.choices).get(form.departments.data)
   
     # Check if user is in the list of existing user and prevent creation
    users =  User.query.all()
    existing_usersIDs = [user.userID for user in users]
    if form.username.data in existing_usersIDs:
        return render_template("auth/new.html", form = form, id_error = "User already exists")

    if not form.validate():
        return render_template("auth/new.html", form = form)
    if form.admin.data == False:
        form.admin.data = 0
    else:
        form.admin.data = 1
  
    
    u = User(form.username.data, form.firstname.data, form.lastname.data, sha256_crypt.hash(form.password.data), form.departments.data, form.admin.data)
    
  
    db.session().add(u)
    db.session().commit()
  
    return redirect(url_for("accounts_index"))