from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email_loginform = StringField("email", validators=[DataRequired()])
    password_loginform = PasswordField("password", validators=[DataRequired()])
    submit_loginform = SubmitField("Log in")


class RegisterForm(FlaskForm):
    email_regform = StringField("email", validators=[DataRequired()])
    password_regform = PasswordField("password", validators=[DataRequired()])
    fio_regform = StringField("fio", validators=[DataRequired()])
    sex_regform = SelectField("sex", choices=['м', 'ж'])
    age_regform = IntegerField()
    submit_regform = SubmitField("Register")
    

class ChooseTimetableDoctor(FlaskForm):
    doctor = SelectField(choices=[])
    date = DateField()
    submit_choose = SubmitField("Choose timetable")


class ExecuteTimetable(FlaskForm):
    time = HiddenField()
    submit_execute = SubmitField("Add record in database")


class UpdateAge(FlaskForm):
    age = IntegerField(validators=[DataRequired()])
    submit = SubmitField("Change age")
