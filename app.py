
import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__  == '__main__':
    app.debug = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()