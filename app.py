import os
from flask import Flask, request, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
# from flask_jwt import JWT ,jwt_required
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
# configuring and setting up database
app.config['SECRET_KEY'] = 'sds_api'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sds_api.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
# jwt = JWT(app, authenticate, identity)
api = Api(app)


# CREATING models

class SDS_Members(db.Model):    
    name = db.Column(db.String(100))
    mis = db.Column(db.Integer(), primary_key=True, nullable=False)
    email = db.Column(db.String())
    since = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(member, name, mis, email):
        member.name = name
        member.mis = mis
        member.email = email

    def json(member):
        return {'Name: ': member.name, 'MIS: ': member.mis, 'Email: ': member.email}

    def __str__(member):
        return f" Name of SDS Member: {member.name}\nMIS: {member.mis}\nEmail: {member.email}"

class SDS_Projects(db.Model):
    projectName = db.Column(db.String(100))
    projectDesc = db.Column(db.String(500))
    mis_projectHead = db.Column(db.Integer(), primary_key=True, nullable=False)
    email_projectHead = db.Column(db.String())
    started = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(project, projectName, projectDesc, mis_projectHead, email_projectHead):
        project.name = projectName
        project.desc = projectDesc
        project.mis = mis_projectHead
        project.email = email_projectHead

    def json(project):
        return {'Name: ': project.name, 'Project Description: ': {project.desc}, 'MIS: ': project.mis, 'Email: ': project.email}

    def __str__(project):
        return f" Name of Project: {project.name}\nProject Description: {project.desc}\nMIS: {project.mis}\nEmail: {project.email}"


# member = SDS_Members(name="SHIKHAR", mis=112003005, email="agarawalsd20.comp@coep.ac.in")
# db.session.add(member)
# db.session.commit()
@app.route("/")
def HomePage():
    return render_template("sds_api_home.html")


@app.route('/members', methods=['GET'])
def read_members():
    if request.method == 'GET':
        members = SDS_Members.query.all()
        return render_template("members.html", get=members)


@app.route('/members/', methods=['GET', 'POST'])
def create_member():
    if request.method == 'GET':
        return render_template("members_form.html")
    if request.method == 'POST':
        name = request.form['Name']
        mis = request.form['MIS']
        email = request.form['Email']

        members = SDS_Members(name, mis, email)
        db.session.add(members)
        db.session.commit()

        flash("Member Inserted Successfully")

        return redirect(url_for('read_members'))


@app.route('/members/delete/<mis>')
def delete_member(mis):
    ex_member = SDS_Members.query.filter_by(mis=mis).first()
    db.session.delete(ex_member)
    db.session.commit()
    return redirect("/members")


@app.route('/members/update/<mis>', methods=['GET', 'POST'])
def update_member(mis):
    member = SDS_Members.query.filter_by(mis=mis).first()
    if request.method == 'GET':
        return render_template("members_update.html", update=member)
    if request.method == 'POST':
        member.name = request.form['Name']
        member.mis = request.form['MIS']
        member.email = request.form['Email']

        # members = SDS_Members(name, mis, email)
        # db.session.update(members)
        db.session.commit()

        flash("Member Updated Successfully")

        return redirect(url_for('read_memebers'))

@app.route('/projects', methods=['GET'])
def read_projects():
    if request.method == 'GET':
        projects = SDS_Projects.query.all()
        return render_template("project.html", get=projects)

@app.route('/projects/', methods=['GET', 'POST'])
def create_project():
    if request.method == 'GET':
        return render_template("projects_form.html")
    if request.method == 'POST':
        Name = request.form['projectName']
        Desc = request.form['projectDesc']
        mis = request.form['Mis_projectHead']
        email = request.form['Email_projectHead']
        # print(request.form['projectName'], ['projectDesc'], ['Mis_projectHead'], ['Email_projectHead'])
        # print(projectName, projectDesc, mis_projectHead, email_projectHead)
        newProject = SDS_Projects(request.form['projectName'], request.form['projectDesc'], request.form['Mis_projectHead'], request.form['Email_projectHead'])
        db.session.add(newProject)
        db.session.commit()

        flash("Project Added Successfully")

        return redirect(url_for('read_projects'))

@app.route('/projects/delete/<projectName>')
def delete_project(projectName):
    old_project = SDS_Projects.query.filter_by(projectName=projectName).first()
    db.session.delete(old_project)
    db.session.commit()
    return redirect("/projects")


if __name__ == "__main__":
    app.run(debug=True)
