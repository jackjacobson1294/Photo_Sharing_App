from flask import *
import extensions
import re
import uuid
import hashlib

album_api = Blueprint('album_api', __name__, template_folder='templates')

@album_api.route('/api/v1/album/<int:album_id>', methods=['GET'])
def album(album_id):
	db = extensions.connect_to_database()
	cur = db.cursor()
	user = ''
	if 'username' in session:
		user = session['username']
	if not album_id:
		error = []
		error.append({'message':"The requested resource could not be found"})
		return jsonify(errors = error),404
    #logged_in = False
    ##check username and stuff in javascript
    #if 'username' in session:
    #    logged_in = True
    #if logged_in:
    #    user = session['username']
    #else:
    #    user = request.args.get('username')
	if album_id < 1:
		error = []
		error.append({'message':"The requested resource could not be found"})
		return jsonify(errors = error),404
	cur.execute('USE group120db')
	cur.execute('SELECT * FROM Album WHERE albumid = %d' % (album_id))
	album_exist = cur.fetchall()
	if not album_exist:
		error = []
		error.append({'message':"The requested resource could not be found"})
		return jsonify(errors = error),404
	album_exist = album_exist[0]
	pictures = []
    #owner = album_exist[0]['username']
    #owner_var = False
    #has_access = False
    #if owner == user:
    #    owner_var = True
    #    has_access = True
    #if album_exist[0]['access'] == 'private':
    #    if not user:
    #        return redirect(url_for('main.login_route'))
    #    else:
    #        cur.execute('SELECT * FROM AlbumAccess WHERE albumid = %d' % (album_id))
    #        users = cur.fetchall()
    #        for person in users:
    #            if person['username'] == user:
    #                has_access = True
    #else:
    #    has_access = True
    #if not has_access:
    #    abort(403)

	cur.execute('SELECT * FROM Contain WHERE albumid = %d' % (album_id))
	pics = cur.fetchall()
	cur.execute('SELECT * FROM Photo')
	photos = cur.fetchall()
	for pic in pics:
		for photo in photos:
			if pic['picid'] == photo['picid']:
				pictures.append({'albumid':album_id,'caption':pic['caption'],'date':photo['picDate'],'format':photo['format'],'picid':pic['picid'],'sequencenum':pic['sequencenum']})
	access = album_exist['access'];
	owner = album_exist['username'];
	if access == "private" :
		if user == '' :
			error = []
			error.append({'message':"You do not have the necessary credentials for the resource"})
			return jsonify(errors = error),401
		else:
			cur.execute('SELECT * FROM AlbumAccess WHERE albumid = %d' % (album_id))
			user_access_albums = cur.fetchall()
			user_acces = False
			for people in user_access_albums:
				if(people['username'] == user):
					user_access = True
			if owner != user:
				if user_access == False:
					error = []
					error.append({'message':"You do not have the necessary permissions for the resource"})
					return jsonify(errors = error),403
	album = ({'access': album_exist['access'],'albumid': album_id, 'created': album_exist['created'], 'lastupdated': album_exist['lastupdated'],'pics': pictures,'title': album_exist['title'],'username': album_exist['username']})
	return jsonify(album = album), 200