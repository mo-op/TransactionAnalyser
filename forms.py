from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

class AnalystForm(FlaskForm):
	gasstation = IntegerField("GasStationID")
	submit = SubmitField("Query")

class LogInForm(FlaskForm):
	username = TextField("Username")
	password = TextField("Password")
	submit = SubmitField("Sign In")