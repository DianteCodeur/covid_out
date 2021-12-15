from covidout import db
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import UserMixin
from covidout import login


from flask_login import current_user


import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
	def __init__(self,**kwargs):
		super(User, self).__init__(**kwargs)
		self.profile = Profile(user=self)

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

	examens = db.relationship('Examen', backref='user', lazy="dynamic",cascade="save-update, merge, delete")
	
	declarationSuspects =db.relationship('DeclarationSuspect', backref='user', lazy="dynamic",cascade="save-update, merge, delete")
	dons = db.relationship('Don', backref='user', lazy="dynamic",cascade="save-update, merge, delete")

	savoirs = db.relationship('Savoir', backref='user', lazy="dynamic",cascade="save-update, merge, delete")


	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {} {} >'.format(self.username,self.id)  


class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.relationship('User',lazy=True,backref='profile',cascade="save-update, merge, delete",uselist=False)
	email = db.Column(db.String(120), index=True, unique=True)
	adresse = db.Column(db.String(120), index=True)
	telephone = db.Column(db.String(20), index=True)
	def __repr__(self):
		return f'<Profile de {self.user} {self.email} {self.adresse},{self.telephone}>'





class Examen(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	age = db.Column(db.String(12), index=True)
	sexe = db.Column(db.String(12), index=True)
	touxrecente = db.Column(db.String(12), index=True)
	respirer = db.Column(db.String(12), index=True)

	fievreSensation = db.Column(db.String(12), index=True)
	fievre = db.Column(db.String(12), index=True)
	malGorge = db.Column(db.String(12), index=True)
	impossibiliteManger = db.Column(db.String(12), index=True)

	courbatures = db.Column(db.String(12), index=True)
	perteOrdorat = db.Column(db.String(12), index=True)
	diarrhee = db.Column(db.String(12), index=True)
	maladieConnu = db.Column(db.String(12), index=True)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def populate_from_form(self,form):
		self.user= current_user
		self.age = form.age.data
		self.sexe = form.sexe.data
		self.touxrecente = form.touxrecente.data
		self.respirer = form.respirer.data
		self.fievreSensation = form.fievreSensation.data
		self.fievre = form.fievre.data
		self.malGorge = form.malGorge.data
		self.impossibiliteManger = form.impossibiliteManger.data
		self.courbatures = form.courbatures.data
		self.perteOrdorat = form.perteOrdorat.data
		self.diarrhee = form.diarrhee.data
		self.maladieConnu = form.maladieConnu.data


    

	def __repr__(self):
		return f'<Examen de {self.user} >'


class Savoir(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	modeTransmission = db.Column(db.String(12), index=True)
	animalCompagnie = db.Column(db.String(12), index=True)
	maniereEviter = db.Column(db.String(12), index=True)
	personneTouche = db.Column(db.String(12), index=True)

	alcool = db.Column(db.String(12), index=True)
	traitement = db.Column(db.String(12), index=True)
	temps = db.Column(db.String(12), index=True)
	comparable = db.Column(db.String(12), index=True)

	climat = db.Column(db.String(12), index=True)
	produitsContamine = db.Column(db.String(12), index=True)


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def populate_from_form(self,form):
		self.user= current_user
		self.modeTransmission = form.modeTransmission.data
		self.animalCompagnie = form.animalCompagnie.data
		self.maniereEviter = form.maniereEviter.data
		self.personneTouche = form.personneTouche.data
		self.alcool = form.alcool.data
		self.traitement = form.traitement.data
		self.temps = form.temps.data
		self.comparable = form.comparable.data
		self.climat = form.climat.data
		self.produitsContamine = form.produitsContamine.data



	def get_note(self):
		note = 0
		for attr, value in self.__dict__.items():
			if value == "V":
				note+=1
		return note


    

	def __repr__(self):
		return f'<Examen de {self.user} >'



class DeclarationSuspect(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	descriptif = db.Column(db.Text)
	lieu = db.Column(db.String(200), index=True)
	
	def __repr__(self):
		return f'<Declaration de {self.user}>'

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def populate_from_form(self,form):
		self.user =current_user
		self.descriptif = form.descriptif.data
		self.lieu = form.lieu.data


class Don(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	descriptif = db.Column(db.Text)	
	
	def __repr__(self):
		return f'<Declaration de {self.user}>'

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def populate_from_form(self,form):
		self.user=current_user
		self.descriptif = form.descriptif.data

		print("Dans le self  ",self.descriptif)


#User(username='susan', email='susan@example.com')
#flask db init 
#flask db migrate
#flask db upgrade

