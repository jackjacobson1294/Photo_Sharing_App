from flask import *
import extensions
import uuid
import hashlib
import re

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def main_route():
	db = extensions.connect_to_database()
	cur = db.cursor()
	cur.execute('use group120db')
	if 'username' in session:
		user = session['username']
		cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
		user_db = cur.fetchall()
		first_name = user_db[0]['firstname']
		last_name = user_db[0]['lastname']
		cur.execute('SELECT * FROM Album WHERE access = "%s"' % ('public'))
		public_albums = cur.fetchall()
		cur.execute('SELECT * FROM AlbumAccess WHERE username = "%s"' % (user))
		user_access_albums = cur.fetchall()
		cur.execute('SELECT * FROM Album WHERE username = "%s" AND access = "%s"' % (user, 'private'))
		private_albums = cur.fetchall()
		cur.execute('SELECT * From Album')
		all_albums = cur.fetchall()
		options = {
			"logged_in": True,
			"firstname" : first_name,
			"lastname" : last_name,
			"public_albums": public_albums,
			"user_access_albums": user_access_albums,
			"private_albums": private_albums,
			"all_albums": all_albums
		}
		return render_template("index.html", **options)
	else:
		cur.execute('SELECT * FROM Album WHERE access = "%s"' % ('public'))
		albums = cur.fetchall()
		cur.execute('SELECT username FROM User')
		users = cur.fetchall()
		options = {
			"logged_in": False,
			"users" : users,
			"public_albums" : albums
		}
		return render_template("index.html", **options)

@main.route('/login', methods=['GET', 'POST'])
def login_route():
	if request.method == 'POST':
		db = extensions.connect_to_database()
		cur = db.cursor()
		cur.execute('use group120db')
		user = request.form.get('username')
		passwd = request.form.get('password')
		blankUser = False
		blankPwd = False
		wrongPwd = False
		noUser = False

		if user == '':
			blankUser = True
			noUser = True
		if passwd == '':
			blankPwd = True
			wrongPwd = True

		cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
		user_exist = cur.fetchall()
		if not user_exist:
			noUser = True
			wrongPwd = True

		if blankUser or blankPwd or noUser:
			if blankUser:
				wrongPwd = False
				noUser = False
			elif noUser:
				blankPwd = False
				wrongPwd = False



			opt = {
				'blankUser': blankUser,
				'blankPwd': blankPwd,
				'wrongPwd': wrongPwd,
				'noUser': noUser
			}
			return redirect(url_for('main.login_route', **opt))
		else:
			algorithm = 'sha512'
			cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
			pd = cur.fetchall()
			new_pd = pd[0]['password']
			salt = new_pd[new_pd.find("$")+1:]
			salt = salt[:salt.find("$")]
			m = hashlib.new(algorithm)
			m.update(salt + passwd)
			password_hash = m.hexdigest()
			finPassword = "$".join([algorithm,salt,password_hash])
			if pd[0]['password'] == str(finPassword):
				session['username'] = user
				session['firstname'] = pd[0]['firstname']
				session['lastname'] = pd[0]['lastname']
				return redirect(url_for('main.main_route'))
			else:
				wrongPwd = True
				opt = {
					'blankUser': blankUser,
					'blankPwd': blankPwd,
					'wrongPwd': wrongPwd,
					'noUser': noUser
				}
				return redirect(url_for('main.login_route', **opt))
	else:
		blankUser = request.args.get('blankUser')
		blankPwd = request.args.get('blankPwd')
		noUser = request.args.get('noUser')
		if blankUser == 'True':
			blankUser = True
		else:
			blankUser = False
		if blankPwd == 'True':
			blankPwd = True
		else:
			blankPwd = False
		wrongPwd = request.args.get('wrongPwd')
		if wrongPwd == 'True':
			wrongPwd = True
		else:
			wrongPwd = False
		if noUser == 'True':
			noUser = True
		else:
			noUser = False
		opt = {
			'blankUser': blankUser,
			'blankPwd': blankPwd,
			'wrongPwd': wrongPwd,
			'noUser': noUser
		}
		return render_template("login.html", **opt)

@main.route('/logout', methods=['POST'])
def logout_route():
	session.pop('username', None)
	session.pop('firstname', None)
	session.pop('lastname', None)
	return redirect(url_for('main.main_route'))

@main.route('/user', methods=['GET', 'POST'])
def newUser_route():
	if request.method == 'POST':
		db = extensions.connect_to_database()
		cur = db.cursor()
		cur.execute('use group120db')
		user = request.form.get('username')
		first = request.form.get('firstname')
		last = request.form.get('lastname')
		eml = request.form.get('email')
		pw1 = request.form.get('password1')
		pw2 = request.form.get('password2')

		temp_lower = user.lower()

		blankUser = False
		blankFirst = False
		blankLast = False
		blankEml = False
		blankPw1 = False
		lenUser = False
		lenFirst = False
		lenLast = False
		uniqueUser = False
		lenUser3 = False
		lenPass = False
		passMatch = False
		specCharsUser = False
		specCharsPass = False
		emailLen = False
		emailSyn = False
		passSyn = False

		specCharsUser = not (all(u.isalnum() or u == '_' for u in user))
		specCharsPass = not (all(u.isalnum() or u == '_' for u in pw1))

		hasLet = False
		hasNum = False 
		for c in pw1:
			if c.isalpha():
				hasLet = True 
			if c.isdigit():
				hasNum = True 
		if not (hasLet and hasNum):
			passSyn = True

		cur.execute('SELECT * FROM User WHERE lower(username) = "%s"' % (temp_lower))
		user_found = cur.fetchall();
		if user_found:
			uniqueUser = True
		
		if user == '':
			blankUser = True
			lenUser3 = True
		elif len(user) > 20:
			lenUser = True
		elif len(user) < 3:
			lenUser3 = True
		if first == '':
			blankFirst = True 
		elif len(first) > 20:
			lenFirst = True
		if last == '':
			blankLast = True 
		elif len(last) > 20:
			lenLast = True
		if eml == '':
			blankEml = True
		elif len(eml) > 40:
			emailLen = True
		if pw1 == '':
			blankPw1 = True
			lenPass = True
		elif len(pw1) < 8:
			lenPass = True
		if pw1 != pw2:
			passMatch = True
		if not re.match(r"[^@]+@[^@]+\.[^@]+", eml):
			emailSyn = True


		if blankUser or blankFirst or blankLast or blankEml or blankPw1 or lenUser or lenFirst or lenLast or uniqueUser or lenUser3 or lenPass or passMatch or specCharsUser or specCharsPass or emailLen or emailSyn or passSyn:
			opt = {
				'blankUser' : blankUser,
				'blankFirst' : blankFirst,
				'blankLast' :blankLast,
				'blankEml' : blankEml,
				'blankPw1' : blankPw1,
				'lenUser': lenUser,
				'lenFirst': lenFirst,
				'lenLast' : lenLast,
				'uniqueUser': uniqueUser,
				'lenUser3': lenUser3,
				'lenPass': lenPass,
				'passMatch': passMatch,
				'specCharsUser': specCharsUser,
				'specCharsPass': specCharsPass,
				'emailLen': emailLen,
				'emailSyn': emailSyn,
				'passSyn': passSyn
			}
			return redirect(url_for('main.newUser_route', **opt))

		else:
			algorithm = "sha512"
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + pw1)
			password_hash = m.hexdigest()
			finPassword = "$".join([algorithm,salt,password_hash])
			cur.execute('INSERT INTO User (username, firstname, lastname, email, password) VALUES ("%s", "%s", "%s", "%s", "%s")' % (user, first, last, eml, finPassword))
			return redirect(url_for('main.login_route'))
	else: 
		if 'username' in session:
			return redirect(url_for('main.user_edit_route'))
		else:
			blankUser = request.args.get('blankUser')
			if blankUser == 'True':
				blankUser = True
			else:
				blankUser = False
			blankFirst = request.args.get('blankFirst')
			if blankFirst == 'True':
				blankFirst = True
			else:
				blankFirst = False
			blankLast = request.args.get('blankLast')
			if blankLast == 'True':
				blankLast = True
			else:
				blankLast= False
			blankEml = request.args.get('blankEml')
			if blankEml == 'True':
				blankEml = True
			else:
				blankEml = False
			blankPw1 = request.args.get('blankPw1')
			if blankPw1 == 'True':
				blankPw1 = True
			else:
				blankPw1 = False
			lenUser = request.args.get('lenUser')
			if lenUser == 'True':
				lenUser = True
			else:
				lenUser = False
			lenFirst = request.args.get('lenFirst')
			if lenFirst == 'True':
				lenFirst = True;
			else:
				lenFirst = False
			lenLast = request.args.get('lenLast')
			if lenLast == 'True':
				lenLast = True
			else:
				lenLast = False
			uniqueUser = request.args.get('uniqueUser')
			if uniqueUser == 'True':
				uniqueUser = True
			else:
				uniqueUser = False
			lenUser3 = request.args.get('lenUser3')
			if lenUser3 == 'True':
				lenUser3 = True
			else:
				lenUser3 = False
			lenPass = request.args.get('lenPass')
			if lenPass == 'True':
				lenPass = True
			else:
				lenPass = False
			passMatch = request.args.get('passMatch')
			if passMatch == 'True':
				passMatch = True
			else:
				passMatch = False
			specCharsUser = request.args.get('specCharsUser')
			if specCharsUser == 'True':
				specCharsUser = True
			else:
				specCharsUser = False
			specCharsPass = request.args.get('specCharsPass')
			if specCharsPass == 'True':
				specCharsPass = True
			else:
				specCharsPass = False
			emailLen = request.args.get('emailLen')
			if emailLen == 'True':
				emailLen = True
			else:
				emailLen = False
			emailSyn = request.args.get('emailSyn')
			if emailSyn == 'True':
				emailSyn = True
			else:
				emailSyn = False
			passSyn = request.args.get('passSyn')
			if passSyn == 'True':
				passSyn = True
			else:
				passSyn = False


			opt = {
				'blankUser' : blankUser,
				'blankFirst' : blankFirst,
				'blankLast' :blankLast,
				'blankEml' : blankEml,
				'blankPw1' : blankPw1,
				'lenUser': lenUser,
				'lenFirst': lenFirst,
				'lenLast': lenLast,
				'uniqueUser': uniqueUser,
				'lenUser3': lenUser3,
				'lenPass': lenPass,
				'passMatch': passMatch,
				'specCharsUser': specCharsUser,
				'specCharsPass': specCharsPass,
				'emailLen': emailLen,
				'emailSyn': emailSyn,
				'passSyn': passSyn
			}
			return render_template("newUser.html", **opt)

@main.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():
	logged_in = False
	if 'username' in session:
		logged_in = True
	if logged_in == False:
		return redirect(url_for('main.login_route'))
	if request.method == 'POST':
		db = extensions.connect_to_database()
		cur = db.cursor()
		cur.execute('use group120db')
		firstLength = False
		lastLength = False
		lenPass = False
		passMatch = False
		specCharsPass = False
		emailLen = False
		emailSyn = False
		passSyn = False
		if request.form.get('firstname'):
			firstname = request.form.get('firstname')
			length = len(firstname);
			if length > 20:
				firstLength = True
			else:
				session['firstname'] = firstname
				cur.execute('UPDATE User SET firstname = "%s" WHERE username = "%s"' % (firstname, session['username']))
		elif request.form.get('lastname'):
			lastname = request.form.get('lastname')
			length = len(lastname)
			if length > 20:
				lastLength = True
			else:
				session['lastname'] = lastname
				cur.execute('UPDATE User SET lastname = "%s" WHERE username = "%s"' % (lastname, session['username']))
		elif request.form.get('email'):
			email = request.form.get('email')
			length = len(email)
			run = True
			if length > 40:
				emailLen = True
				run = False
			if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
				emailSyn = True
				run = False
			if run:
				cur.execute('UPDATE User SET email = "%s" WHERE username = "%s"' % (email, session['username']))
		elif request.form.get('password1'):
			password1 = request.form.get('password1')
			password2 = request.form.get('password2')
			length = len(password1)
			run = True
			if length < 8:
				lenPass = True
				run = False
			if password1 != password2:
				passMatch = True
				run = False
			specCharsPass = not (all(u.isalnum() or u == '_' for u in password1))

			hasLet = False
			hasNum = False 

			for c in password1:
				if c.isalpha():
					hasLet = True 
				if c.isdigit():
					hasNum = True 
			if not (hasLet and hasNum):
				passSyn = True
				run = False
			algorithm = "sha512"
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hash = m.hexdigest()
			finPassword = "$".join([algorithm,salt,password_hash])
			if run and not specCharsPass:
				cur.execute('UPDATE User SET password = "%s" WHERE username = "%s"' % (finPassword, session['username']))
		if firstLength or lastLength or lenPass or passMatch or specCharsPass or emailLen or emailSyn or passSyn:
			opt = {
				'firstLength': firstLength,
				'lastLength': lastLength,
				'lenPass': lenPass,
				'passMatch': passMatch,
				'specCharsPass': specCharsPass,
				'emailLen': emailLen,
				'emailSyn': emailSyn,
				'passSyn': passSyn
			}
			return redirect(url_for('main.user_edit_route', **opt))
		else:
			return redirect(url_for('main.user_edit_route'))
	else: 
		first = request.args.get('firstLength')
		last = request.args.get('lastLength')
		lenPwd = request.args.get('lenPass')
		match = request.args.get('passMatch')
		firstLen = False
		lastLen = False
		lenPass = False
		passMatch = False
		if first == 'True':
			firstLen = True
		if last == 'True':
			lastLen = True
		if lenPwd == 'True':
			lenPass = True
		if match == 'True':
			passMatch = True
		specCharsPass = request.args.get('specCharsPass')
		if specCharsPass == 'True':
			specCharsPass = True
		else:
			specCharsPass = False
		emailLen = request.args.get('emailLen')
		if emailLen == 'True':
			emailLen = True
		else:
			emailLen = False
		emailSyn = request.args.get('emailSyn')
		if emailSyn == 'True':
			emailSyn = True
		else:
			emailSyn = False
		passSyn = request.args.get('passSyn')
		if passSyn == 'True':
			passSyn = True
		else:
			passSyn = False
		opt = {
			'firstLength': firstLen,
			'lastLength': lastLen,
			'lenPass': lenPass,
			'passMatch': passMatch,
			'specCharsPass': specCharsPass,
			'emailLen': emailLen,
			'emailSyn': emailSyn,
			'passSyn': passSyn
		}
		return render_template("userEdit.html", **opt)

	

	