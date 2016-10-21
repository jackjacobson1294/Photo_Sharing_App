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
		if first == '':
			blankFirst = True 
		elif len(first) > 20:
			lenFirst = True
			errors.append({"message":"Firstname must be no longer than 20 characters"})
		if last == '':
			blankLast = True 
		elif len(last) > 20:
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
			errors = {
				'message': "You did not provide the necessary fields"
			}
			return jsonify(errors), 422

		if lenUser or lenFirst or lenLast or uniqueUser or lenUser3 or lenPass or passMatch or specCharsUser or specCharsPass or emailLen or emailSyn or passSyn:
			return jsonify(errors), 422
		
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
		return jsonify(userDict), 201
