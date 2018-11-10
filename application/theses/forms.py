from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SelectMultipleField, validators

class ThesisForm(FlaskForm):
    title = StringField("Thesis working title", [validators.Length(min=2)])
    description = TextAreaField("Description", [validators.Length(min=5)])
    #todo link to Sciences
    science = SelectMultipleField('Languages', choices = [('1', 'Economics'), 
      ('2', 'Computer science')])
 
    class Meta:
        csrf = False