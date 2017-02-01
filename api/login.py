from flask import *
import extensions
import uuid
import hashlib
import re

login = Blueprint('login', __name__, template_folder='templates')

@login.route("/api/v1/login", methods=['POST'])
def loginAPI():
	db = extensions.connect_to_database()
	cur = db.cursor()
	cur.execute('use maindb')
	json_obj = request.get_json();
	user = str(json_obj[('username')])
	passwd = str(json_obj[('password')])
	blankUser = False
	blankPwd = False
	wrongPwd = False
	noUser = False

	errors = []

	if not user:
		blankUser = True
		noUser = True
		errors.append({'message' : 'You did not provide the necessary fields'})
		return jsonify(errors = errors), 422
	if not passwd:
		blankPwd = True
		wrongPwd = True

	cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
	user_exist = cur.fetchall()
	if not user_exist:
		noUser = True
		wrongPwd = True
		errors.append({'message' : 'Username does not exist'})
		return jsonify(errors=errors), 404
		"""
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
		"""
	#else:
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
	if pd[0]['password'] != str(finPassword):
		errors.append({'message': 'Password is incorrect for the specified username'})
		return jsonify(errors=errors), 422
	else:
		session['username'] = user
		session['firstname'] = pd[0]['firstname']
		session['lastname'] = pd[0]['lastname']
		data = {
			"username": user
		}
		return jsonify(data=data), 200
	"""
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
	"""