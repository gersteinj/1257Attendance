from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SignInForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    first = StringField('First Name')
    last = StringField('Last Name')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Sign In')
