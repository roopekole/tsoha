from flask_wtf import FlaskForm
from wtforms import StringField, validators

  
class SciForm(FlaskForm):
    name = StringField("Science name:", [validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    
  
    class Meta:
        csrf = False