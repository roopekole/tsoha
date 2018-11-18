from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.theses.models import Thesis
from application.theses.forms import ThesisForm, ThesisEditForm
from application.science.models import Science
from application.auth.models import User
from application.departments.models import Dept
from application.models import science2thesis
import sys

@app.route("/theses", methods=["GET"])
def theses_index():
    theses = Thesis.query.all()
    statuses = ["Available","Progressing","Completed"]
    depts = Dept.query.all()

    return render_template("theses/list.html", theses = theses, statuses = statuses, depts = depts)

@app.route("/theses/new/")
@login_required
def theses_form():

    #Fetch available sciences
    sciences = Science.query.all()

    form = ThesisForm(username = current_user.userID)
    form.science.choices = [(science.scienceID, science.name) for science in sciences]

    return render_template("theses/new.html", form = form)

  
@app.route("/theses/<thesis_id>/", methods=["GET"])
@login_required
def thesis_edit(thesis_id):
   
    t = Thesis.query.get(thesis_id)
   
    if not (t.userID == current_user.userID or current_user.admin):
        
        return "Access denied2"
    
    # Get the thesis details pre-filled for editing / viewing
    form = ThesisEditForm(obj=t, username = t.userID, level = t.level, createdon = t.createdOn, modifiedon = t.modifiedOn)
    
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
    t.title = form.title.data
    t.description = form.description.data
    # WTF form returns string instead of boolean
    if form.level.data == "True":
        level = True
    else:
        level = False
    t.level = level
    t.author = form.author.data
    t.status = form.status.data

    
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


    #if not form.validate():
     #   return render_template("theses/new.html", form = form)


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