from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectField, validators
from wtforms.fields.html5 import EmailField
  
class LoginForm(FlaskForm):
    username = EmailField('Email address', [validators.DataRequired(), validators.Email()], render_kw={"class": "form-control"})
    password = PasswordField("Password", [validators.DataRequired()], render_kw={"class": "form-control"})
  
    class Meta:
        csrf = False

class NewAccountForm(FlaskForm):
    username = EmailField('Email address:', [validators.DataRequired(), validators.Email()], render_kw={"class": "form-control"})
    password = PasswordField("Password:", [validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    firstname = StringField("First name:",[validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    lastname = StringField("Last name:",[validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    departments = SelectField('Department',  render_kw={"class": "form-control"})
    admin = BooleanField("Make an admin")
  
    class Meta:
        csrf = False

class AccountForm(FlaskForm):
    username = EmailField('Email address:', [validators.DataRequired(), validators.Email()], render_kw={"readonly class": "form-control"})
    password = PasswordField("Password:", [validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    firstname = StringField("First name:",[validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    lastname = StringField("Last name:",[validators.Length(min=2, max=144)], render_kw={"class": "form-control"})
    departments = SelectField('Department',  render_kw={"class": "form-control"})
    admin = BooleanField("Make an admin")
  
    class Meta:
        csrf = False