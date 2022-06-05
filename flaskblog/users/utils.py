import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)	#yukledigin resin dosyasinin adini degistirir digerleri ile karismasin diye.
	_, f_ext = os.path.splitext(form_picture.filename) #random hex .jpg yi .png yi degistirmesin die.
	picture_fn = random_hex + f_ext	#random hex + file extension
	picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

	#yuklenen fotonun boyutunu kucultme
	output_size = (500, 500) 
	i = Image.open(form_picture) #yuklenen resmi ac onu i ye at
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Şifre sıfırlama.',
                  sender='bozuk:(@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Sıfırlamak için linke tıkla:
{url_for('users.reset_token', token=token, _external=True)}
Bunu sen istemediysen bu maili görmezden gel.
'''
    mail.send(msg)