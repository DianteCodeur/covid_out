from flask import render_template, flash, redirect,request,url_for,request

from form import *
from models import *
from covidout import app

from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.urls import url_parse

from helper import *


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('client/index.html', title='Sign In',slider=slider)

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    return render_template('client/stats.html')


@app.route('/examen', methods=['GET', 'POST'])
@login_required
def examen():
    form = ExamenForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            obj = Examen()
            obj.populate_from_form(form)
            obj.save_to_db()

            flash(f"Super ! Vous avez bien rempli vous recevrez un mail avec les résultats ",'info')
            return redirect(url_for("examen"))

        elif request.method == 'POST':
            flash(f"Remplissez toutes les questions s'il vous plaît",'error')
            print(form.errors)
    return render_template('client/examen.html',form=form)



@app.route('/don', methods=['GET', 'POST'])
@login_required
def don():
    form = DonForm()
    if request.method == 'POST':
        form = DonForm(formdata=request.form)
        if form.validate_on_submit():
            obj = Don()
            obj.populate_from_form(form)
            obj.save_to_db()

            flash(f"Super ! Votre don a été pris en compte ",'info')

            return redirect(url_for('don'))

        elif request.method == 'POST':
            flash(f"Remplissez correctement  svp",'error')
            print(form.errors)
    return render_template('client/DonForm.html',form=form,titre="Faites un don ")



@app.route('/savoir', methods=['GET', 'POST'])
@login_required
def savoir():
    form = SavoirForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            obj = Savoir()
            obj.populate_from_form(form)
            obj.save_to_db()



            flash(f"Super ! Votre savoir a été pris en compte ",'info')
            return redirect(url_for("savoir"))

        elif request.method == 'POST':
            flash(f"Remplissez correctement  svp",'error')
            print(form.errors)
    return render_template('client/savoir.html',form=form,titre="Testons vos connaissances ")



@app.route('/declaration', methods=['GET', 'POST'])
@login_required
def declaration():
    form = DeclarationForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            obj = DeclarationSuspect()
            obj.populate_from_form(form)
            obj.save_to_db()

            flash(f"Super ! Votre declaration a été prise en compte ",'info')
            return redirect(url_for('declaration'))

        elif request.method == 'POST':
            flash(f"Remplissez correctement  svp",'error')
            print(form.errors)
    return render_template('client/DonForm.html',form=form,titre="Faites une déclaration ( informez des cas suspects) ")






@app.route('/connexion', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Nom d'utilisateur ou mot de passe incorrect")
                return redirect(url_for('login'))
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('profile')
            return redirect(next_page)

    return render_template('client/login.html', title='Sign In', form=form)



@app.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    form=ProfileForm(formdata=request.form, obj=current_user.profile)
    print(current_user.profile)
    if request.method == 'POST' and form.validate_on_submit():

        current_user.username= form.username.data
        current_user.profile.email=form.email.data
        current_user.profile.adresse = form.adresse.data 
        current_user.profile.telephone = form.telephone.data 

        print("Num de telephone",current_user.profile.telephone)
        db.session.add(current_user)
        db.session.commit()

        flash(f"Votre profile est enregistré {current_user.username}")
    else:
        form.username.data=current_user.username
    return render_template('client/form.html', form=form,titre="Mon Profile")


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Vous vous êtes bien inscris !')
        return redirect(url_for('login'))
    return render_template('client/register.html', title='Register', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


