import secrets
import os
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from Application import app, db, bcrypt
from Application.forms import RegForm, LogForm, NewNote, NewTag, EditNote, NewFile
from Application.models import User, Note, Tag, TagNoteLink, File
from sqlalchemy import and_

@app.route("/", methods=['GET','POST'])
def home():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	else:
		return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegForm()
	if form.validate_on_submit():
		hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hash_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	form = LogForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_pg = request.args.get('next')
			return redirect(next_pg) if next_pg else redirect(url_for('account'))
		else:
			flash('Login failed', 'danger')
	return render_template('login.html', title='login', form=form)

@app.route("/logout", )
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/editNote<cn>", methods=['GET','POST'])
@login_required
def editNote(cn):
	app.current_edit = cn
	return redirect(url_for("account"))

@app.route("/notes", methods=['GET','POST'])
@login_required
def notes():
	app.current_tag = '/~'
	app.current_path = '/~'
	return redirect(url_for("account"))

@app.route("/notes", methods=['GET','POST'])
@login_required
def files():
	app.current_tag = '/~'
	app.current_path = '/~'
	return redirect(url_for("account"))


@app.route("/selectTag<cn>", methods=['GET','POST'])
@login_required
def selectTag(cn):
	if cn != '~':
		app.current_tag = cn
	else:
		app.current_tag = '/~'
	return redirect(url_for("account"))

@app.route("/deleteNote<cn>", methods=['GET','POST'])
@login_required
def deleteNote(cn):
	for tnl in TagNoteLink.query.filter_by(note=cn).all():
		db.session.delete(tnl)
	db.session.delete(Note.query.filter_by(name=cn).first())
	db.session.commit()
	return redirect(url_for("account"))

@app.route("/deleteTag<ct>", methods=['GET','POST'])
@login_required
def deleteTag(ct):
	for tnl in TagNoteLink.query.filter_by(tag=ct).all():
		db.session.delete(tnl)
	db.session.delete(Tag.query.filter_by(name=ct).first())
	db.session.commit()
	if ct == app.current_tag:
		app.curent_tag='/~'
	return redirect(url_for("account"))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	if app.current_tag == '/~':
		notes = Note.query.filter_by(author=current_user).filter_by(path=app.current_path)
	else:
		notes = Note.getByTag(app.current_tag)

	print(app.current_path)


	note = NewNote()
	tag = NewTag()
	file = NewFile()



	if app.current_edit != '/~':

		edit = EditNote()

		if edit.validate_on_submit():
			app.current_edit = '/~'
			note_update = Note.query.get_or_404(app.current_edit_id)
			note_update.name = edit.name.data
			note_update.content = edit.content.data
			db.session.commit()
			edit = None
			return redirect(url_for("account"))
		elif request.method == 'GET':
			editN = Note.query.filter_by(name=app.current_edit).first()
			edit.name.data = editN.name
			edit.content.data = editN.content
			tags = ""
			for tt in TagNoteLink.query.filter_by(note=app.current_edit):
				tags = tags + tt.tag + " "
			edit.tags.data = tags
			app.current_edit_id = editN.id
	else:
		edit = None

		if note.validate_on_submit():

			tags = note.tags.data.split(" ")

			for tt in tags:
				tag_aux = Tag.query.filter_by(name=tt).first()
				if tag_aux != None:

					if Tag.query.filter_by(name=tt).first():
						print(tt)
						link = TagNoteLink(note=note.name.data, tag=tt)
						db.session.add(link)
						db.session.commit()

			n = Note(name=note.name.data, content=note.content.data, author=current_user, path=app.current_path)
			db.session.add(n)
			db.session.commit()
			flash(f'Note created')



	if tag.validate_on_submit():
		createTag(tag)
		return redirect(url_for('account'))


	if file.validate_on_submit():
		createFile(file)
		return redirect(url_for('account'))
	if file.is_submitted():
		print(File.query.filter_by(owner=current_user.id, name=file.name1.data, path=app.current_path).first(), app.current_path)

	return render_template('account.html', title='Account', note=note, notes=notes, tag=tag, tags=getTags(), file=file, files=getFiles(), edit=edit)


def createTag(tag):
	t = Tag(name=tag.name2.data, author1=current_user)
	db.session.add(t)
	db.session.commit()
	flash(f'Tag created')


def createFile(file):
	f = File(name=file.name1.data, author2=current_user, path=app.current_path)
	db.session.add(f)
	db.session.commit()
	flash(f'File created')


@app.route("/cancel",methods=['GET','POST'])
def cancel():
	app.current_edit = '~'
	return redirect(url_for('account'))

@app.route("/tagPress<f>",methods=['GET','POST'])
def tagPress(f):
	print(f)
	return redirect(url_for('account'))

def getTags():
	if current_user.is_authenticated:
		t = Tag.query.filter_by(author1=current_user)

		return t
	else:
		return None

def getFiles():
	if current_user.is_authenticated:
		a = File.query.filter_by(author2=current_user, path=app.current_path)

		return a
	else:
		return None

@app.route("/toFile<file>", methods=['GET', 'POST'])
def toFile(file):
	app.current_path = app.current_path + "/" + file

	return redirect(url_for('account'))


@app.route("/back", methods=['GET', 'POST'])
def back():
	if app.current_path != '/~':
		app.current_path = app.current_path[:app.current_path.rfind('/')]

	return redirect(url_for('account'))

