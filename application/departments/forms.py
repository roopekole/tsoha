from flask_wtf import FlaskForm
from wtforms import StringField, validators

  
class DeptForm(FlaskForm):
    name = StringField("Deparment name:", [validators.DataRequired()], render_kw={"class": "form-control"})
    
  
    class Meta:
        csrf = False