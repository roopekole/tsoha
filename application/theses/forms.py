from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SelectMultipleField, SelectField, RadioField, DateTimeField, validators

class ThesisForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title", [validators.Length(min=2)],  render_kw={"class": "form-control"})
    description = TextAreaField("Description", [validators.Length(min=5)],  render_kw={"class": "form-control"})
    # List passed from route
    science = SelectMultipleField('Science(s)',  render_kw={"multiple class": "form-control"})
 
    class Meta:
        csrf = False

class ThesisEditForm(FlaskForm):
    username = StringField("Supervisor", render_kw={"readonly class": "form-control"})
    title = StringField("Thesis working title", [validators.Length(min=2)],  render_kw={"class": "form-control"})
    description = TextAreaField("Description", [validators.Length(min=5)],  render_kw={"class": "form-control"})
    # List passed from route
    science = SelectMultipleField('Science(s)',  render_kw={"multiple class": "form-control"})
    level = RadioField('Level', choices=[(False, 'Bachelor'), (True, 'Master')],  render_kw={" class": "form-check-input"})

    # Todo: validation between author and status, if author selected -> status cannot be available
    author = StringField("Author", [validators.Length(min=2)],  render_kw={"class": "form-control"})
    status = SelectField("Status", choices=[(0, 'Available'), (1, 'In progress'),(2, 'Completed')], render_kw={"class": "form-control"} )
    createdon = DateTimeField("Created on", render_kw={"readonly class": "form-control"})
    modifiedon = DateTimeField("Modified on", render_kw={"readonly class": "form-control"})
    class Meta:
        csrf = False