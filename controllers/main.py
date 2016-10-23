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
	return render_template("login.html")

@main.route('/logout', methods=['POST'])
def logout_route():
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


	

	