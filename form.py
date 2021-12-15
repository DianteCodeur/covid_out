from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField , IntegerField,SelectField,RadioField ,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,required ,length
from models import User


from wtforms.widgets.html5 import NumberInput


import phonenumbers
from models import *
from validate_email import validate_email as ve


from helper import qSav ,qEx

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeter le mot de passe', validators=[DataRequired(), EqualTo('password',message='Les mots de passe ne correspondent pas')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Nom d'utilisateur existant")

    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError("Le mot de passe doit contenir au moins 4 caractères")




class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    """
    def validate_username(self, username):
        if len(username.data) < 3 :
            raise ValidationError("Nom d'utilisateur doit contenir au moins 3 caractères")"""

class ProfileForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()])
    adresse = StringField('Adresse')
    email = StringField('Email')
    telephone = StringField('Numéro de téléphone')

    def validate_email(self,email):
        if email.data:
            if ve(email.data)==False:
                raise ValidationError('Email invalide')
        else:
            print("pas d'email")

    def validate_telephone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Numéro de téléphone invalide')


class ExamenForm(FlaskForm):
    age = IntegerField(widget=NumberInput())
    sexe=RadioField(qEx["sexe"]["q"], choices=qEx["sexe"]["c"])
    touxrecente = RadioField(qEx["touxrecente"]["q"], choices=qEx["touxrecente"]["c"])
    respirer = RadioField(qEx["respirer"]["q"], choices=qEx["respirer"]["c"])

    fievreSensation = RadioField(qEx["fievreSensation"]["q"], choices=qEx["fievreSensation"]["c"])
    fievre = RadioField(qEx["fievre"]["q"], choices=qEx["fievre"]["c"])
    malGorge = RadioField(qEx["malGorge"]["q"], choices=qEx["malGorge"]["c"])
    impossibiliteManger = RadioField(qEx["impossibiliteManger"]["q"], choices=qEx["impossibiliteManger"]["c"])
    
    courbatures = RadioField(qEx["courbatures"]["q"], choices=qEx["courbatures"]["c"])
    perteOrdorat = RadioField(qEx["perteOrdorat"]["q"], choices=qEx["perteOrdorat"]["c"])
    diarrhee = RadioField(qEx["diarrhee"]["q"], choices=qEx["diarrhee"]["c"])
    maladieConnu = RadioField(qEx["maladieConnu"]["q"], choices=qEx["maladieConnu"]["c"])


class SavoirForm(FlaskForm):
    modeTransmission=RadioField(qSav["modeTransmission"]["q"], choices=qSav["modeTransmission"]["c"])
    animalCompagnie = RadioField(qSav["animalCompagnie"]["q"], choices=qSav["animalCompagnie"]["c"])

    maniereEviter=RadioField(qSav["maniereEviter"]["q"], choices=qSav["maniereEviter"]["c"])
    personneTouche=RadioField(qSav["personneTouche"]["q"], choices=qSav["personneTouche"]["c"])

    alcool=RadioField(qSav["alcool"]["q"], choices=qSav["alcool"]["c"])
    traitement=RadioField(qSav["traitement"]["q"], choices=qSav["traitement"]["c"])
    temps=RadioField(qSav["temps"]["q"], choices=qSav["temps"]["c"])
    comparable=RadioField(qSav["comparable"]["q"], choices=qSav["comparable"]["c"])
    climat=RadioField(qSav["climat"]["q"], choices=qSav["climat"]["c"])
    produitsContamine=RadioField(qSav["produitsContamine"]["q"], choices=qSav["produitsContamine"]["c"])
 



class DeclarationForm(FlaskForm):
    lieu = StringField("Le lieu de l'évènement")
    descriptif = TextAreaField(f"Que se passe t'il concrètement ?", [required(),length(max=200)])
    
class DonForm(FlaskForm):
    descriptif = TextAreaField(u'Décrivez nous ce que vous aimeriez donner et grâce à votre adresse nous viendrons récupérer 😊 ', [required(),length(max=200)])
    


