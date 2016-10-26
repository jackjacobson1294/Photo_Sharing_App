from flask import *
import extensions

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET','POST'])
def pic_route():
	# db = extensions.connect_to_database()
	# cur = db.cursor()
	# if request.method == "POST":
	# 	pic_id = request.form.get('picid')
	# else:
	# 	pic_id = request.args.get('picid')
	# cur.execute('USE group120db')
	# op = request.form.get('op')
	# cur.execute('SELECT * FROM Photo WHERE picid = "%s"' % (pic_id))
	# pic = cur.fetchall()
	# if not pic:
	# 	abort(404)
	# cur.execute('SELECT * FROM Contain WHERE picid = "%s"' % (pic_id))
	# pic_in_contain = cur.fetchall()
	# album_id = -1
	# if len(pic_in_contain) != 0:
	# 	album_id = pic_in_contain[0]['albumid']
	# owner = False
	# logged_in = False
	# if 'username' in session:
	# 	logged_in = True
	# if logged_in:
	# 	user = session['username']
	# else:
	# 	user = request.args.get('username')
	# cur.execute('SELECT * FROM Album WHERE albumid = "%s"' % (album_id))
	# alb = cur.fetchall()
	# if alb[0]['username'] == user:
	# 	owner = True
	# if owner == False:
	# 	if alb[0]['access'] == "private":
	# 		cur.execute('SELECT * From AlbumAccess WHERE username = "%s"' % user)
	# 		access_albums = cur.fetchall()
	# 		can_view = False
	# 		for aa in access_albums:
	# 			if aa['albumid'] == alb[0]['albumid']:
	# 				can_view = True
	# 	else:
	# 		can_view = True
	# else:
	# 	can_view = True
	# if can_view == False:
	# 	if logged_in:
	# 		abort(403)
	# 	else:
	# 		return redirect(url_for("main.login_route"))
	# if not op:
	# 	cur.execute('SELECT * FROM Contain WHERE albumid = %d' %  (album_id))
	# 	album = cur.fetchall()
	# 	prevID = ''
	# 	nextID = ''
	# 	for i in range(0, len(album)):
	# 		if(album[i]['picid'] == pic_id):
	# 			if(len(album) != 1):
	# 				if(i != 0 and i != len(album) - 1):
	# 					prevID = album[i - 1]['picid']
	# 					nextID = album[i + 1]['picid']
	# 				elif(i == 0):
	# 					nextID = album[i + 1]['picid']
	# 				else:
	# 					prevID = album[i - 1]['picid']
	# 	options = {
	#         "album": album,
	#         "album_id": album_id,
	#         "pic" : pic,
	#         "pic_in_contain": pic_in_contain,
	#         "prevID": prevID,
	#         "nextID": nextID, 
	#         "owner": owner
	#     }

	# 	return render_template("pic.html", **options)
	# else:
	# 	caption = request.form.get('caption')
	# 	cur.execute('UPDATE Contain SET caption = "%s" WHERE picid = "%s"' % (caption, pic_id))
	# 	cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
	# 	return redirect(url_for("pic.pic_route", picid = pic_id))
	return render_template("album.html")	





