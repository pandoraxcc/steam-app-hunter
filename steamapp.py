from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask import url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from core import app
from helpers import ProcessHelper

# Routing for the app

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        return ProcessHelper.process_url()

    return render_template('index.html')

@app.route('/profile-submission', methods=['GET'])
def redirect_submission():
    return redirect(url_for('index', _anchor='profile-submission'))

if __name__  == '__main__':
    app.debug = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()