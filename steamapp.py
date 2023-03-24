import re
import flask_excel as excel
import csv
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_paginate import Pagination, get_page_parameter
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from core import app
from models import db, Users, SteamProfiles
from helpers import ProcessHelper


# Route for the home page
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        return ProcessHelper.process_url()

    return render_template('index.html')

# Route for rendering the results page
@app.route('/profile-submission', methods=['GET'])
def redirect_submission():
    return redirect(url_for('index', _anchor='profile-submission'))

# Registration route 
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "GET":

        return render_template("register.html")

    elif request.method == "POST":
        
        submitted_username = request.form.get('username')
        submitted_password = request.form.get('password')
        confirmed_password = request.form.get('password2')

        if not submitted_username or not submitted_password or not confirmed_password:

            flash('Please fill all fileds')
            return redirect('/register')

        if submitted_password != confirmed_password:

            flash('Passwords are not matching')
            return redirect('/register')

        if 3 > (len(submitted_username) or len(submitted_password)):

            flash('Username and password must be > 3 symbols')
            return redirect('/register')
        
        space_in_inputs_login = re.search(" ", submitted_username)
        space_in_inputs_password = re.search(" ", submitted_password)
        
        if space_in_inputs_login or space_in_inputs_password :

            flash("You can't use space in login/password")
            return redirect('/register')

        else:
            pass

    username_check = db.session.query(Users).filter_by(username=submitted_username).first()

    if username_check is None:
        pass

    else:

        flash('Username is already in use')
        return redirect('/register')

    p_hash = generate_password_hash(submitted_password)
    new_user = Users(username=submitted_username, password=p_hash )
    db.session.add(new_user)
    db.session.commit()

    registered_id = db.session.query(Users).filter_by(username=submitted_username).first()
    registered_id = registered_id.id
    session['user_id'] = registered_id

    return render_template("index.html")

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        log_username = request.form.get('username')
        log_pass = request.form.get('password')

        if not log_username or not log_pass:
            flash('Please fill both fileds')
            return redirect('/login')

        user_data = db.session.query(Users).filter_by(username=log_username).first()

        if user_data is not None:
  
            if check_password_hash(user_data.password, log_pass):
                session['user_id'] = user_data.id
                return redirect('/')
            else:
                flash('Incorrect username or password')
                return redirect('/login')

        else:
            flash('Incorrect username or password')
            return redirect('/login')
    
    else: 
        return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Route for the faq page
@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

# Route for history page
ROWS_PER_PAGE = 5
@app.route('/history', methods=['GET'])
def history():
    try:
        if session['user_id']:

            page = request.args.get('page', 1, type=int)
            results = db.session.query(SteamProfiles).filter(SteamProfiles.user_id==session['user_id']).paginate(page=page, per_page=ROWS_PER_PAGE)
            results_db = db.session.query(SteamProfiles).filter(SteamProfiles.user_id==session['user_id']).all()
            
            total_profiles = len(results_db)
            records_in_db = len(results.items)
            hours_2_weeks_total = 0
            inactive_users = 0
            
            for element in results_db:
                if element.hours_in_2_weeks == 0:
                    inactive_users += 1
                hours_2_weeks_total += element.hours_in_2_weeks

            return render_template('history.html', results=results, records_in_db=records_in_db, hours_2_weeks_total=hours_2_weeks_total, total_profiles=total_profiles, inactive_users=inactive_users)
        
        else:
            return redirect('/')
    except KeyError:
        return redirect('/')

# Route for exporting the history
@app.route('/get-history', methods=['GET', 'POST'])
def get_history():
    if request.method == "GET":

        try:

            if session['user_id']:

                now = datetime.now()
                timestamp = str(datetime.timestamp(now))
                filename = 'export' + timestamp + '.csv'
                header = ['steam_username', 'hours_in_2_weeks', 'steam_profile_id']
                data = db.session.query(SteamProfiles).filter(SteamProfiles.user_id==session['user_id']).all()
                extracted = []
                table_header = ['Username', 'Hours', 'Steam Profile Url']
                
                for record in data:
                    tmp_arr = []
                    tmp_arr.extend((record.steam_username, record.hours_in_2_weeks, record.steam_profile_id))
                    extracted.append(tmp_arr)
                extracted.insert(0, table_header)
                excel.init_excel(app)
                extension_type = "csv"
                return excel.make_response_from_array(extracted, file_type=extension_type, file_name=filename)
            
            else:
                return redirect('/')

        except KeyError:
            return redirect('/')
    else:
        return redirect('/history')
        
if __name__  == '__main__':
    app.run()