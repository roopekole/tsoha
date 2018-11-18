from flask_wtf import FlaskForm
from wtforms import StringField, validators

  
class DeptForm(FlaskForm):
    name = StringField("Deparment name:", [validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    
  
    class Meta:
        csrf = False