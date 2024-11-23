# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I started university as a Supply Chain Management Major.','I have a pet maltipoo.','I did the IB program in high school.'])
	return render_template('home.html', fun_fact = x)

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')


@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    db = database()

    feedback_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "comment": request.form.get("comment")
    }
    db.insertRows("feedback", ["name", "email", "comment"], [[feedback_data["name"], feedback_data["email"], feedback_data["comment"]]])
    all_feedback = db.query("SELECT name, comment FROM feedback")
    return render_template("processfeedback.html", feedback=all_feedback)



