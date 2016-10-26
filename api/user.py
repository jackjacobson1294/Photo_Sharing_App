from flask import *
import extensions
import re
import uuid
import hashlib

user = Blueprint('user', __name__, template_folder='templates')

@user.route("/api/v1/user", methods=['POST','GET','PUT'])
def userPost():
	if request.method == "POST":
		db = extensions.connect_to_database()
		cur = db.cursor()
		cur.execute('use group120db')
		json_obj = request.get_json();
		user = str(json_obj['username'])
		first = str(json_obj['firstname'])
		last = str(json_obj['lastname'])
		eml = str(json_obj['email'])
		pw1 = str(json_obj['password1'])
		pw2 = str(json_obj['password2'])

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

		errors = []

		hasLet = False
		hasNum = False 
		for c in pw1:
			if c.isalpha():
				hasLet = True 
			if c.isdigit():
				hasNum = True 
		if not (hasLet and hasNum):
			errors.append({"message":"Passwords may only contain letters, digits, and underscores"})
			passSyn = True

		cur.execute('SELECT * FROM User WHERE lower(username) = "%s"' % (temp_lower))
		user_found = cur.fetchall();
		if user_found:
			uniqueUser = True
			errors.append({"message":"This username is taken"})
		if user == '':
			blankUser = True
			lenUser3 = True
		elif len(user) > 20:
			lenUser = True
			errors.append({"message":"Username must be no longer than 20 characters"})
		elif len(user) < 3:
			lenUser3 = True
			errors.append({"message":"Username must be at least 3 characters long"})
		if len(first) > 20:
			lenFirst = True
			errors.append({"message":"Firstname must be no longer than 20 characters"})
		if len(last) > 20:
			lenLast = True
			errors.append({"message":"Lastname must be no longer than 20 characters"})
		if eml == '':
			blankEml = True
		elif len(eml) > 40:
			emailLen = True
			errors.append({"message":"Email must be no longer than 40 characters"})
		if pw1 == '':
			blankPw1 = True
			lenPass = True
		elif len(pw1) < 8:
			lenPass = True
			errors.append({"message":"Passwords must be at least 8 characters long"})
		if pw1 != pw2:
			passMatch = True
			errors.append({"message":"Passwords do not match"})
		if not re.match(r"[^@]+@[^@]+\.[^@]+", eml):
			emailSyn = True
			errors.append({"message":"Email address must be valid"})
		if blankUser or blankFirst or blankLast or blankEml or blankPw1:
			errors = []
			errors.append({'message':"You did not provide the necessary fields"})
			return jsonify(errors = errors), 422

		if lenUser or lenFirst or lenLast or uniqueUser or lenUser3 or lenPass or passMatch or specCharsUser or specCharsPass or emailLen or emailSyn or passSyn:
			return jsonify(errors = errors), 422
		
		else:
			algorithm = "sha512"
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + pw1)
			password_hash = m.hexdigest()
			finPassword = "$".join([algorithm,salt,password_hash])
			cur.execute('INSERT INTO User (username, firstname, lastname, email, password) VALUES ("%s", "%s", "%s", "%s", "%s")' % (user, first, last, eml, finPassword))
		
		userDict = {
			'username': user,
			'firstname': first,
			'lastname': last,
			'email': eml
		}
		return jsonify(data = userDict), 201

	elif request.method == "PUT":
		logged_in = False;
		if 'username' in session:
			logged_in = True;
		else:
			errors = []
			errors.append({'message':'You do not have the necessary credentials for the resource'})
			return jsonify(errors = errors), 401
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
		blankEml = False
		passEmpty = False

		json_obj = request.get_json();
		firstname = str(json_obj['firstname'])
		lastname = str(json_obj['lastname'])
		email = str(json_obj['email'])
		password1 = str(json_obj['password1'])
		password2 = str(json_obj['password2'])

		errors = []

		if firstname!='':
			length = len(firstname);
			if length > 20:
				firstLength = True
				errors.append({'message':'Firstname must be no longer than 20 characters'})
			#CHANGE THIS
			#else:
			#	session['firstname'] = firstname
		if lastname!='':
			length = len(lastname)
			if length > 20:
				lastLength = True
				errors.append({'message':'Lastname must be no longer than 20 characters'})
			#else:
			#	session['lastname'] = lastname
			#	cur.execute('UPDATE User SET lastname = "%s" WHERE username = "%s"' % (lastname, session['username']))
		if email!='':
			length = len(email)
			if length > 40:
				emailLen = True
				errors.append({'message':'Email must be no longer than 40 characters'})
			if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
				emailSyn = True
				errors.append({'message':'Email address must be valid'})
			#if run:
			#	cur.execute('UPDATE User SET email = "%s" WHERE username = "%s"' % (email, session['username']))
		else:
			blankEml = True

		if password1!='':
			length = len(password1)
			if length < 8:
				errors.append({'message':'Passwords must be at least 8 characters long'})
				lenPass = True
			if password1 != password2:
				passMatch = True
				errors.append({'message':'Passwords do not match'})
			specCharsPass = not (all(u.isalnum() or u == '_' for u in password1))
			errors.append({'message':'Passwords may only contain letters, digits, and underscores'})

			hasLet = False
			hasNum = False 

			for c in password1:
				if c.isalpha():
					hasLet = True 
				if c.isdigit():
					hasNum = True 
			if not (hasLet and hasNum):
				passSyn = True
				errors.append({'message':'Passwords must contain at least one letter and one number'})
			#algorithm = "sha512"
			#salt = uuid.uuid4().hex
			#m = hashlib.new(algorithm)
			#m.update(salt + password1)
			#password_hash = m.hexdigest()
			#finPassword = "$".join([algorithm,salt,password_hash])
			#if run and not specCharsPass:
			#	cur.execute('UPDATE User SET password = "%s" WHERE username = "%s"' % (finPassword, session['username']))
		else:
			if password2!='':
				passMatch = True
				errors.append({'message':'Passwords do not match'})
			else:
				passEmpty = True

		if blankEml:
			errors = []
			errors.append({'message':'You did not provide the necessary fields'})
			return jsonify(errors = errors), 422
		if firstLength or lastLength or lenPass or passMatch or specCharsPass or emailLen or emailSyn or passSyn:
			return jsonify(errors = errors), 422
		else:
			session['firstname'] = firstname
			session['lastname'] = lastname
			cur.execute('UPDATE User SET firstname = "%s" WHERE username = "%s"' % (firstname, session['username']))
			cur.execute('UPDATE User SET lastname = "%s" WHERE username = "%s"' % (lastname, session['username']))
			cur.execute('UPDATE User SET email = "%s" WHERE username = "%s"' % (email, session['username']))
			if not passEmpty:
				algorithm = "sha512"
				salt = uuid.uuid4().hex
				m = hashlib.new(algorithm)
				m.update(salt + password1)
				password_hash = m.hexdigest()
				finPassword = "$".join([algorithm,salt,password_hash])
				cur.execute('UPDATE User SET password = "%s" WHERE username = "%s"' % (finPassword, session['username']))
				
			userDict = {
				'username': session['username'],
				'firstname': session['firstname'],
				'lastname': session['lastname'],
				'email': email
			}
			return jsonify(data = userDict), 201
	elif request.method == "GET":
		logged_in = False

		if 'username' in session:
			logged_in = True;
		else:
			logged_in = False
			errors = []
			errors.append({'message':'You do not have the necessary credentials for the resource'})
			return jsonify(errors = errors), 401
		db = extensions.connect_to_database()
		cur = db.cursor()
		cur.execute('use group120db')
		cur.execute('SELECT * FROM User WHERE username = "%s"' % (session['username']))
		eml = cur.fetchall()
		email = eml[0]['email']
		userDict = {
			'username': session['username'],
			'firstname': session['firstname'],
			'lastname': session['lastname'],
			'email': email
		}

		return jsonify(data = userDict), 201

