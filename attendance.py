from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
import datetime
from airtable import Airtable
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
os.environ['AIRTABLE_API_KEY'] = config.API_KEY

with open('scans.csv', 'a') as f:
    f.write('timestamp,student_id,first,last\n')

at = Airtable(config.BASE_ID, 'Improved Attendance')

def get_record_id_by_student_id(student_id):
  record = at.search('Student ID', student_id)
  return record[0]['id']

def at_sign_in(student_id, column='unset'):
  record_id = get_record_id_by_student_id(student_id)
  at.update(record_id, fields={column:'Present'})

## FORMS ##
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


## VIEWS ##
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        # flash(f'Sign in for user {student_id}')
        # at_record_id = get_record_id_by_student_id(student_id)
        try:
            at_sign_in(student_id, column='unset')
            with open('scans.csv', 'a') as f:
                f.write(f"{datetime.datetime.now()},{student_id},-,-\n")
                flash(f"Logged in student id: {student_id}")
            return redirect('/signin')
        except:
            flash('No user found!')
            return redirect('/register')
    return render_template('signinform.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        with open('scans.csv', 'a') as f:
            f.write(f"{datetime.datetime.now()},{student_id},{form.first.data},{form.last.data}\n")
        flash(f"Saved info for {form.first.data} {form.last.data} (student id: {student_id})")
        return redirect('/signin')
    return render_template('registerform.html', form=form)