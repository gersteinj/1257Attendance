from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import SignInForm, RegisterForm
from airtable import Airtable
from app import config
import datetime

at = Airtable(config.BASE_ID, 'Improved Attendance')

def get_record_id_by_student_id(student_id):
    record = at.search('Student ID', student_id)
    return record[0]['id']

def at_sign_in(student_id, column='unset'):
    record_id = get_record_id_by_student_id(student_id)
    at.update(record_id, fields={column:'Present'})

@app.route('/')
def index():
    return render_template('index.html')

with open('scans.csv', 'a') as f:
    f.write('timestamp,student_id,first,last\n')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        try:
            at_sign_in(student_id, column='unset')
            flash(f"Okay, I'll sign in user {student_id}")
            with open('scans.csv', 'a') as f:
                f.write(f"{datetime.datetime.now()},{student_id},-,-\n")
            return redirect(url_for('signin'))
        except:
            flash('No such user!')
            return redirect(url_for('register', student_id=student_id))
    return render_template('signinform.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        student_id = request.args['student_id']
        flash(f"Stored info for {form.first.data} {form.last.data} (student id: {student_id}) so you can scan in next time")
        with open('scans.csv', 'a') as f:
            f.write(f"{datetime.datetime.now()},{student_id},{form.first.data},{form.last.data}\n")
        return redirect('/signin')
    return render_template('registerform.html', form=form)