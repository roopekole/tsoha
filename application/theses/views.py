from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from sqlalchemy import func
from application.theses.models import Thesis
from application.theses.forms import ThesisForm, ThesisEditForm, ThesisCheckoutForm, ThesisSearch
from application.science.models import Science
from application.auth.models import User
from application.departments.models import Dept
from application.models import science2thesis
import sys
import datetime


@app.route("/theses", methods=['GET', 'POST'])
def theses_index():
    
    search_values = ThesisSearch(request.form)

    # Initialize the search form for the user after reset
    if request.method == 'POST' and request.form['action'] == 'Reset':
        search_values = None

    statuses = ["Available","Progressing","Completed"]
   
    # Define search form
    form = ThesisSearch()

    # Add choices for sciences
    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]


    # Add choices for departments
    depts = Dept.query.all()
    form.departments.choices = [(department.departmentID, department.name) for department in depts]


    
    # Add choices for statuses, hardcoded
    form.status.choices = [(0,"Available"),(1,"Progressing"),(2,"Completed")]

    search = False
    #If search has been applied with criteria. If no criteria show all
    if request.method == 'POST' and request.form['action'] == 'Search' and len(search_values.departments.data+search_values.science.data+search_values.supervisor.data+search_values.status.data)>0:
        
         # Results by science - join through association
        thesis_by_science = Thesis.query.join(science2thesis).join(Science).filter(science2thesis.c.scienceID.in_(search_values.science.data)).all()
        print(thesis_by_science)
        # Results by theses's status and user id - easy relations with direct relations ships and foreign keys
        theses_by_status_user = Thesis.query.filter(Thesis.status.in_(search_values.status.data) | Thesis.userID.in_(search_values.supervisor.data)).all()
        # Results by department - join department by thesis user
        theses_by_department = Thesis.query.join(User).filter(User.department.in_(search_values.departments.data)).all()
        # Merge results to single list, remove duplicates ,sort alphabetically by Thesis.title
        theses = sorted(list(set(theses_by_status_user + theses_by_department + thesis_by_science)), key=lambda t: t.title.lower())
    else:
        # Fetch all theses, sort alphabetically by Thesis.title
        theses = Thesis.query.order_by(func.lower(Thesis.title)).all()
    
    #Pagination
    def get_theses(offset=0, per_page=10):
        return theses[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter="page",
                                           per_page_parameter="per_page")
    total = len(theses)
    paginated_theses = get_theses(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework="bootstrap4", record_name="theses")

    # Add choices for users who are thesis supervisors
    userids = [thesis.userID for thesis in theses]
    unique_ids = list(set(userids))

    user_details = User.query.filter(User.userID.in_(unique_ids)).all()
    form.supervisor.choices = [(user.userID, user.firstName + " " + user.lastName) for user in user_details]
        
    
    return render_template("theses/list.html", form = form, theses = paginated_theses, statuses = statuses, depts = depts, page=page, per_page = per_page, pagination = pagination)


@app.route("/theses/new/")
@login_required
def theses_form():

    #Fetch available sciences
    sciences = Science.query.all()

    form = ThesisForm(username = current_user.userID)
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    return render_template("theses/new.html", form = form)

@app.route("/theses/finalize/<thesis_id>")
@login_required
def thesis_finalize(thesis_id):

    t = Thesis.query.get(thesis_id)
    # Allow finalizing thesis only if user is admin or the supervisor of the thesis and the thesis is in progress
    if not ((t.userID == current_user.userID  or current_user.admin) and t.status == 1):
        return "Access denied"
    t.status = 2
    t.completedOn = datetime.datetime.now()
    db.session().commit()

    return redirect(url_for("theses_index"))

@app.route("/theses/clear_checkout/<thesis_id>")
@login_required
def thesis_clear_checkout(thesis_id):

    t = Thesis.query.get(thesis_id)
    # Allow clearing student checkout only if user is admin and the thesis is available
    if not (current_user.admin and t.status == 1):
        return "Access denied"

    t.status = 0
    t.level = None
    t.completedOn = None
    t.author = None
    t.reservedOn = None
    db.session().commit()

    return redirect(url_for("theses_index"))

  
@app.route("/theses/<thesis_id>/", methods=["GET"])
@login_required
def thesis_edit(thesis_id):
   
    t = Thesis.query.get(thesis_id)
    
    # Allow accessing thesis editor only if user is admin or the supervisor of the thesis and the thesis is available
    if not ((t.userID == current_user.userID and t.status == 0) or current_user.admin):
        
        return "Access denied"
    
    # Get the thesis details pre-filled for editing / viewing
    form = ThesisEditForm(obj=t, username = t.userID, createdon = t.createdOn, modifiedon = t.modifiedOn)
    
    #Fetch available sciences
    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    #Fetch selected sciences
    thesis_scis = Science.query.join(science2thesis).join(Thesis).filter(science2thesis.c.thesisID == t.thesisID and science2thesis.c.scienceID == Science.scienceID).all()
    form.science.process_data([(sci.scienceID)  for sci in thesis_scis])
    
    return render_template("theses/edit.html", thesis = t, form = form)

@app.route("/theses/modify/<thesis_id>/", methods=["POST"])
@login_required
def thesis_modify(thesis_id):
   
   
    t = Thesis.query.get(thesis_id)
    
    # Allow accessing thesis editor only if user is admin or the supervisor of the thesis and the thesis is available
    if not ((t.userID == current_user.userID and t.status == 0) or current_user.admin):
       
        return "Access denied"
    form = ThesisEditForm(request.form)

    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    if not form.validate():
        print(form.errors)
        return render_template("theses/edit.html", thesis = t, form = form)

    t.title = form.title.data
    t.description = form.description.data
        
    # Fetch the form science id's and the current science associations
    # Remove existing associations which are not selected
    # Add the new associations from the form
    thesis_scis = Science.query.join(science2thesis).join(Thesis).filter(science2thesis.c.thesisID == t.thesisID and science2thesis.c.scienceID == Science.scienceID).all()
    science_ids = form.science.data 
    
    for id in science_ids:
        s = Science.query.get(id)
        # this will add new non existing associations
        if not(s in thesis_scis):
            t.sciences.append(s)
            db.session().commit()
        if s in thesis_scis:
            thesis_scis.remove(s)
    
           
    removable_scis = thesis_scis
         
 
    for removable_sci in removable_scis:
        s = Science.query.get(removable_sci.scienceID)
        t.sciences.remove(s)

    db.session().commit()        

    if request.form['action'] == 'Save':
        return redirect(url_for("theses_index"))
    elif request.form['action'] == 'Checkout for a student (and save)':
        return redirect(url_for("thesis_checkout_get", thesis_id=t.thesisID))

@app.route("/theses/checkout/<thesis_id>/", methods=["GET"])
@login_required
def thesis_checkout_get(thesis_id):
   
    t = Thesis.query.get(thesis_id)
   
    # Allow accessing thesis checkout editor only if user is admin or the supervisor of the thesis and the thesis is available
    if not ((t.userID == current_user.userID and t.status == 0) or current_user.admin):
        
        return "Access denied"
    
    # Get the thesis details pre-filled for editing / viewing
    form = ThesisCheckoutForm(obj=t, username = t.userID, createdon = t.createdOn, modifiedon = t.modifiedOn)
    
    #Fetch available sciences
    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    #Fetch selected sciences
    thesis_scis = Science.query.join(science2thesis).join(Thesis).filter(science2thesis.c.thesisID == t.thesisID and science2thesis.c.scienceID == Science.scienceID).all()
    form.science.process_data([(sci.scienceID)  for sci in thesis_scis])

    
    return render_template("theses/checkout.html", thesis = t, form = form)

@app.route("/theses/checkout/<thesis_id>/", methods=["POST"])
@login_required
def thesis_checkout(thesis_id):
   
   
    t = Thesis.query.get(thesis_id)
    
    # Allow accessing thesis editor only if user is admin or the supervisor of the thesis and the thesis is available
    if not ((t.userID == current_user.userID and t.status == 0) or current_user.admin):
       
        return "Access denied"

    if request.form['action'] == 'Clear student checkout':
        return redirect(url_for("thesis_clear_checkout", thesis_id=thesis_id))
    else:
        form = ThesisCheckoutForm(request.form)

        sciences = Science.query.all()
        form.science.choices = [(science.scienceID, science.name) for science in sciences]
        form.level.choices = [(False, "Bachelor"), (True, "Master")]

        if not form.validate():
            return render_template("theses/checkout.html", thesis = t, form = form)

    
        t.level = form.level.data
        print("###################")
        print(t.level)

        t.author = form.author.data
        t.status = 1
        t.reservedOn = datetime.datetime.now()
        t.completedOn = None

        db.session().commit()        
    
        return redirect(url_for("theses_index"))


@app.route("/theses/delete/<thesis_id>/", methods=["POST"])
@login_required
def thesis_delete(thesis_id):
   
    t = Thesis.query.get(thesis_id)
    #only admins can delete theses
    if not current_user.admin:
       
        return "Access denied"

  
    #Remove sciences from association table
    thesis_scis = Science.query.join(science2thesis).join(Thesis).filter(science2thesis.c.thesisID == t.thesisID and science2thesis.c.scienceID == Science.scienceID).all()
    for sci in thesis_scis:
        print(sci.scienceID)
        t.sciences.remove(sci)
    db.session().commit()

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("theses_index"))



@app.route("/theses/", methods=["POST"])
def theses_create():
        
    form = ThesisForm(request.form)
    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    if not form.validate():
        return render_template("theses/new.html", form = form)

    t = Thesis(form.title.data, form.description.data, current_user.userID)
    # Get the attached sciences
    science_ids = form.science.data 
      
    db.session().add(t)
    db.session().commit()
    # Get newly created Thesis object
    db.session.refresh(t)

    for id in science_ids:
        s = Science.query.get(id)
        # Add associations to science2thesis
        t.sciences.append(s)
        db.session().commit()

    
    
    return redirect(url_for("theses_index"))