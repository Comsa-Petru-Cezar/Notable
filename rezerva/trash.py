'''
@app.route("/notes<st>", methods=['GET','POST'])
@login_required
def notes(st=None):
	notes = Note.getByTag(st)
	note = NewNote()


	tag = NewTag()

	if note.validate_on_submit():
		tags = note.tags.data.split(" ")

		for t in tags:

			if Tag.query.filter_by(name=t).first().name == t:

				print(t)
				link = TagNoteLink(note=note.name.data, tag=t)
				db.session.add(link)
				db.session.commit()
		note = Note(name=note.name.data, content=note.content.data, author=current_user,)
		db.session.add(note)
		db.session.commit()
		flash(f'Note created')

		return redirect(url_for('notes_all'))

	if tag.validate_on_submit():
		tag = Tag(name=tag.name.data, author1=current_user)
		db.session.add(tag)
		db.session.commit()
		flash(f'Tag created')
		return redirect(url_for('notes_all'))

	return render_template('notes.html', note=note, notes=notes, t=st, tags=getTags())

@app.route("/notesEdit<en><t>", methods=['GET','POST'])
@login_required
def notesEdit(en, t):
	if t == '~':
		notes = Note.query.filter_by(author=current_user)
	else:
		notes = Note.getByTag(t)
	edit = EditNote()

	if edit.validate_on_submit():
		return redirect(url_for("account", t=t))
	editN = Note.query.filter_by(name=en).first()
	edit.name.data = editN.name
	edit.content.data = editN.content
	tags = ""
	for tt in TagNoteLink.query.filter_by(note=en):
		tags = tags + tt.tag + " "
	edit.tags.data = tags
	return render_template('account.html', notes=notes, t=t, edit=edit)

@app.route("/notes_all", methods=['GET','POST'])
@login_required
def notes_all():
	for tnl in TagNoteLink.query.all():
		print(tnl.note, tnl.tag)

	note = NewNote()

	notes = Note.query.filter_by(author=current_user)
	tag = NewTag()

	if note.validate_on_submit():
		tags = note.tags.data.split(" ")

		for t in tags:
			tag_aux = Tag.query.filter_by(name=t).first()
			if tag_aux != None:

				if Tag.query.filter_by(name=t).first():
					print(t)
					link = TagNoteLink(note=note.name.data, tag=t)
					db.session.add(link)
					db.session.commit()
		note = Note(name=note.name.data, content=note.content.data, author=current_user)
		db.session.add(note)
		db.session.commit()
		flash(f'Note created')

		return redirect(url_for('notes_all'))

	if tag.validate_on_submit():
		tag = Tag(name=tag.name.data, author1=current_user)
		db.session.add(tag)
		db.session.commit()
		flash(f'Tag created')
		return redirect(url_for('notes_all'))


	return render_template('notes.html', note=note, notes=notes, tag=tag, tags=getTags())

@app.route("/files", methods=['GET','POST'])
@login_required
def files():
	fileform = NewFile()
	if fileform.validate_on_submit():
		file = File(name=fileform.name.data, author2=current_user, p=0)
		db.session.add(file)
		db.session.commit()
		return redirect(url_for("files"))
	return render_template('files.html', fileform=fileform)'''