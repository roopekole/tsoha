from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
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

    statuses = ["Available","Progressing","Completed"]
    if request.method == 'POST':
        print("############")
        print(search_values.science.data)
        print(search_values.supervisor.data)
        print(search_values.status.data)
    
    theses = Thesis.query.all()
    depts = Dept.query.all()

    # Define search form
    form = ThesisSearch()

    # Add choices for departments
    form.departments.choices = [(department.departmentID, department.name) for department in depts]

    # Add choices for sciences
    sciences = Science.query.all()
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    # Add choices for statuses, hardcoded
    form.status.choices = [(0,"Available"),(1,"Progressing"),(2,"Completed")]

    # Add choices for users who are thesis supervisors
    userids = [thesis.userID for thesis in theses]
    unique_ids = list(set(userids))

    user_details = User.query.filter(User.userID.in_(unique_ids)).all()
    form.supervisor.choices = [(user.userID, user.firstName + " " + user.lastName) for user in user_details]
    
    return render_template("theses/list.html", form = form, theses = theses, statuses = statuses, depts = depts)


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
    t.status = 2
    t.completedOn = datetime.datetime.now()
    db.session().commit()

    return redirect(url_for("theses_index"))

@app.route("/theses/clear_checkout/<thesis_id>")
@login_required
def thesis_clear_checkout(thesis_id):

    t = Thesis.query.get(thesis_id)
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
   
    if not (t.userID == current_user.userID or current_user.admin):
        
        return "Access denied2"
    
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
    
    if not (t.userID == current_user.userID or current_user.admin):
       
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

    
    # todo: if status in progress -> reserved date not null, if completed -> completed date not null

    if request.form['action'] == 'Save':
        return redirect(url_for("theses_index"))
    elif request.form['action'] == 'Checkout for a student (and save)':
        return redirect(url_for("thesis_checkout_get", thesis_id=t.thesisID))

@app.route("/theses/checkout/<thesis_id>/", methods=["GET"])
@login_required
def thesis_checkout_get(thesis_id):
   
    t = Thesis.query.get(thesis_id)
   
    if not (t.userID == current_user.userID or current_user.admin):
        
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
    
    if not (t.userID == current_user.userID or current_user.admin):
       
        return "Access denied"

    if request.form['action'] == 'Clear student checkout':
        return redirect(url_for("thesis_clear_checkout", thesis_id=thesis_id))
    else:
        form = ThesisCheckoutForm(request.form)

        sciences = Science.query.all()
        form.science.choices = [(science.scienceID, science.name) for science in sciences]
    

        if not form.validate():
            return render_template("theses/checkout.html", thesis = t, form = form)

    
        t.level = form.level.data
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