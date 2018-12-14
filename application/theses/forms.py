from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SelectMultipleField, SelectField, RadioField, DateTimeField, validators

class ThesisForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title", [validators.Length(min=2, max=500)],  render_kw={"class": "form-control"})
    description = TextAreaField("Description", [validators.Length(min=5, max=500)],  render_kw={"class": "form-control"})
    # List passed from route
    science = SelectMultipleField('Science(s)',coerce=int,  render_kw={"class": "chosen-select"})
 
    class Meta:
        csrf = False

class ThesisViewForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title",  render_kw={"readonly class": "form-control"})
    description = TextAreaField("Description",  render_kw={"readonly class": "form-control"})
    science = SelectMultipleField('Science(s)',coerce=int,  render_kw={"readonly class": "chosen-select"})
    level = RadioField("Level", choices=[(0, 'Bachelor'), (1, 'Master')], coerce=int, render_kw={"disabled clases": "form-check"})
    status = StringField("Status", render_kw={"readonly class": "form-control"} )
    createdon = DateTimeField("Created on", render_kw={"readonly class": "form-control"})
    modifiedon = DateTimeField("Modified on", render_kw={"readonly class": "form-control"})
    
    class Meta:
        csrf = False

class ThesisEditForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title", [validators.Length(min=2, max=144)],  render_kw={"class": "form-control"})
    description = TextAreaField("Description", [validators.Length(min=5, max=500)],  render_kw={"class": "form-control"})
    # List passed from route
    science = SelectMultipleField('Science(s)',coerce=int,  render_kw={"class": "chosen-select"})
    createdon = DateTimeField("Created on", render_kw={"readonly class": "form-control"})
    modifiedon = DateTimeField("Modified on", render_kw={"readonly class": "form-control"})
    class Meta:
        csrf = False

class ThesisCheckoutForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title", [validators.Length(min=2, max=144)],  render_kw={"readonly class": "form-control"})
    description = TextAreaField("Description", [validators.Length(min=5, max=500)],  render_kw={"readonly class": "form-control"})
    # List passed from route
    science = SelectMultipleField('Science(s)',coerce=int,  render_kw={"readonly class": "chosen-select"})
    level = RadioField('Level', choices=[(0, 'Bachelor'), (1, 'Master')], coerce=int, render_kw={" class": "form-check-input"})

    # Todo: validation between author and status, if author selected -> status cannot be available
    author = StringField("Author", [validators.Length(min=2, max=144)],  render_kw={"class": "form-control"})
    createdon = DateTimeField("Created on", render_kw={"readonly class": "form-control"})
    modifiedon = DateTimeField("Modified on", render_kw={"readonly class": "form-control"})
    class Meta:
        csrf = False

class ThesisSearch(FlaskForm):
    science = SelectMultipleField('Science:',coerce=int,  render_kw={"class": "chosen-select", "data-placeholder":"..."})
    departments = SelectMultipleField('Department:', coerce=int,  render_kw={"class": "chosen-select", "data-placeholder":"..."})
    supervisor = SelectMultipleField('Supervisor:', coerce=str,  render_kw={"class": "chosen-select", "data-placeholder":"..."})
    status = SelectMultipleField('Status:', coerce=int,  render_kw={"class": "chosen-select", "data-placeholder":"..."})
