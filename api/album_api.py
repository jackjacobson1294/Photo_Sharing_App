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
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
    #logged_in = False
    ##check username and stuff in javascript
    #if 'username' in session:
    #    logged_in = True
    #if logged_in:
    #    user = session['username']
    #else:
    #    user = request.args.get('username')
	if album_id < 1:
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
	cur.execute('USE group120db')
	cur.execute('SELECT * FROM Album WHERE albumid = %d' % (album_id))
	album_exist = cur.fetchall()
	if not album_exist:
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
	album_exist = album_exist[0]
	pics = []
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
	pictures = cur.fetchall()
	cur.execute('SELECT * FROM Photo')
	photos = cur.fetchall()
	for pic in pictures:
		for photo in photos:
			if pic['picid'] == photo['picid']:
				pics.append({'albumid':album_id,'caption':pic['caption'],'date':photo['picDate'],'format':photo['format'],'picid':pic['picid'],'sequencenum':pic['sequencenum']})
	access = album_exist['access'];
	owner = album_exist['username'];
	if access == "private" :
		if user == '' :
			errors = []
			errors.append({'message':"You do not have the necessary credentials for the resource"})
			return jsonify(errors = errors),401
		else:
			cur.execute('SELECT * FROM AlbumAccess WHERE albumid = %d' % (album_id))
			user_access_albums = cur.fetchall()
			user_access = False
			for people in user_access_albums:
				if(people['username'] == user):
					user_access = True
			if owner != user:
				if user_access == False:
					errors = []
					errors.append({'message':"You do not have the necessary permissions for the resource"})
					return jsonify(errors = errors),403
	#album = {'access': album_exist['access'],'albumid': album_id, 'created': album_exist['created'], 'lastupdated': album_exist['lastupdated'],'pics': pics,'title': album_exist['title'],'username': album_exist['username']}
	return jsonify({'access': album_exist['access'],'albumid': album_id, 'created': album_exist['created'], 'lastupdated': album_exist['lastupdated'],'pics': pics,'title': album_exist['title'],'username': album_exist['username']}), 200
