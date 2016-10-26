from flask import *
import extensions
import re
import uuid
import hashlib

pic_api = Blueprint('pic_api', __name__, template_folder='templates')

@pic_api.route('/api/v1/pic/<pic_id>', methods=['GET', 'PUT'])
def pic(pic_id):
	db = extensions.connect_to_database()
	cur = db.cursor()
	user = ''
	logged_in = False
	if 'username' in session:
		logged_in = True
		user = session['username']
	if not pic_id:
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
	cur.execute('USE group120db')
	cur.execute('SELECT * FROM Photo WHERE picid = "%s"' % (pic_id))
	pic = cur.fetchall()
	if not pic:
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
	cur.execute('SELECT * FROM Contain WHERE picid = "%s"' % (pic_id))
	pic_in_contain = cur.fetchall()
	album_id = -1
	if len(pic_in_contain) != 0:
		album_id = pic_in_contain[0]['albumid']
		print album_id;
	else:
		errors = []
		errors.append({'message':"The requested resource could not be found"})
		return jsonify(errors = errors),404
	owner = False
	can_view = False
	cur.execute('SELECT * FROM Album WHERE albumid = "%s"' % (album_id))
	alb = cur.fetchall()
	if alb[0]['username'] == user:
		owner = True
		can_view = True
	if owner == False:
		if alb[0]['access'] == "private":
			if logged_in:
				cur.execute('SELECT * From AlbumAccess WHERE username = "%s"' % user)
				access_albums = cur.fetchall()
				for aa in access_albums:
					if aa['albumid'] == alb[0]['albumid']:
						can_view = True
			else:
				errors = []
				errors.append({'message':"You do not have the necessary credentials for the resource"})
				return jsonify(errors=errors),401
		else:
			can_view = True
	if can_view == False:
		if logged_in:
			errors = []
			errors.append({'message':"You do not have the necessary permissions for the resource"})
			return jsonify(errors=errors),403
		else:
			errors = []
			errors.append({'message':"You do not have the necessary credentials for the resource"})
			return jsonify(errors=errors), 401
	cur.execute('SELECT * FROM Contain WHERE albumid = %d' % (album_id))
	albid = cur.fetchall()
	caption = pic_in_contain[0]['caption']
	prevID = ''
	nextID = ''
	for i in range(0, len(albid)):
		if(albid[i]['picid'] == pic_id):
			if(len(albid) != 1):
				if(i != 0 and i != len(albid) - 1):
					prevID = albid[i - 1]['picid']
					nextID = albid[i + 1]['picid']
				elif(i == 0):
					nextID = albid[i + 1]['picid']
				else:
					prevID = albid[i - 1]['picid']
	if request.method == "PUT":
		caption = request.get_json(['caption'])['caption']
		if  not caption:
			errors = []
			errors.append({'message':"You did not provide the necessary fields"})
			return jsonify(errors = errors), 422
		else:
			cur.execute('UPDATE Contain SET caption = "%s" WHERE picid = "%s"' % (caption, pic_id))
			cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
	tempFormat = pic[0]['format']
	pic = {'albumid': alb[0]['albumid'], 'caption': caption, 'format': tempFormat, 'next': nextID, 'picid': pic_id, 'prev': prevID}
	return jsonify(pic=pic), 200

