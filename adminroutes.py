from flask import render_template, flash, redirect,request,url_for,request

from form import *
from models import *
from covidout import app

from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.urls import url_parse

from helper import *




@app.route('/ad/examen/liste/')
def examen_liste():
	examens = Examen.query.all()
	return render_template('admin/examens/liste.html',examens=examens)

@app.route('/ad/examen/<id>')
def examen_voir(id):
	examen = Examen.query.get(id)
	return render_template('admin/examens/voir.html',examen=examen)



@app.route('/ad/don/liste/')
def don_liste():
	dons = Don.query.all()
	return render_template('admin/dons/liste.html',dons=dons)

@app.route('/ad/don_voir/<id>')
def don_voir(id):
	don = Don.query.get(id)
	return render_template('admin/dons/voir.html',don=don)


@app.route('/ad/declaration/liste/')
def declaration_liste():
	declarations = DeclarationSuspect.query.all()
	return render_template('admin/declarations/liste.html',declarations=declarations)

@app.route('/ad/declaration_voir/<id>')
def declaration_voir(id):
	declaration = DeclarationSuspect.query.get(id)
	return render_template('admin/declarations/voir.html',declaration=declaration)



@app.route('/ad/savoir/liste/')
def savoir_liste():
	savoirs = Savoir.query.all()
	return render_template('admin/savoir/liste.html',savoirs=savoirs)

@app.route('/ad/savoir/<id>')
def savoir_voir(id):
	savoir = Savoir.query.get(id)
	return render_template('admin/savoir/voir.html',savoir=savoir)
