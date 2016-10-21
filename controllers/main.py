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
	if 'username' in session:
		return redirect(url_for('main.user_edit_route'))
	return render_template("newUser.html")

@main.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():
	if 'username' in session:
		return render_template("userEdit.html")
	else:
		return redirect(url_for('main.login_route'))


	

	