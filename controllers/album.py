from flask import *
import extensions
import os, sys
import hashlib
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
album = Blueprint('album', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
album = Blueprint('album', __name__, template_folder='templates')

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
    db = extensions.connect_to_database()
    cur = db.cursor()
    cur.execute('USE maindb')
    logged_in = False
    if 'username' in session:
        logged_in = True
    if logged_in:
        user = session['username']
    else:
        return redirect(url_for('main.login_route'))
    op = request.form.get('op')
    if not op:
        album_id = request.args.get('albumid')
        if not album_id:
            abort(404) #HERE
        album_id = int(album_id)
        if album_id < 1:
            abort(404)
        cur.execute('SELECT * FROM Album WHERE albumid = %d' % (album_id))
        album_exist = cur.fetchall()
        if not album_exist:
            abort(404)
        owner = album_exist[0]['username']
        if owner != user:
            abort(403)
        access = album_exist[0]['access']
        if access == "public":
            access = True
        else:
            access = False
        cur.execute('SELECT * FROM Contain WHERE albumid = %d' % (album_id))
        pics = cur.fetchall()
        cur.execute('SELECT * FROM Photo')
        photos = cur.fetchall()
        cur.execute('SELECT * FROM AlbumAccess WHERE albumid = %d' % (album_id))
        users_with_access = cur.fetchall()
        options = {
            "edit": True,
            "album_id": album_id,
            "photos": photos,
            "pics": pics,
            "users_with_access": users_with_access,
            "access": access
        }
        return render_template("album_edit.html", **options)
    else:
        album_id = request.form.get('albumid')
        if not album_id:
            abort(404) #HERE
        album_id = int(album_id)
        if album_id < 1:
            abort(404)
        cur.execute('SELECT * FROM Album WHERE albumid = %d' % (album_id))
        album_exist = cur.fetchall()
        if not album_exist:
            abort(404)
        if op == "delete":
            picid = request.form.get('picid')
            if not picid:
                abort(404)
            cur.execute('SELECT * FROM Contain WHERE picid = "%s"' % (picid))
            picids = cur.fetchall()
            if not picids:
                abort(404)
            cur.execute('DELETE FROM Contain WHERE picid = "%s"' % (picid))
            for pic in picids:
                cur.execute('SELECT format FROM Photo WHERE picid = "%s"' % pic['picid'])
                pic_format = cur.fetchall()[0]['format'];
                if not pic_format:
                    abort(404)
                cur.execute('DELETE FROM Photo WHERE picid = "%s"' % (picid))
                os.remove('static/images/' + picid + "." + str(pic_format))
            cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
        elif op == "add":
            file_name = request.files['file']
            temp_file_name = file_name.filename
            album_id = request.form.get('albumid')
            if not album_id:
                abort(404)
            album_id = int(album_id)
            if album_id < 1:
                abort(404)
            #reload page if the file format is bad 
            pic_format = temp_file_name[-3:]
            m = hashlib.md5(str(album_id) + temp_file_name)
            pic_id = m.hexdigest()
            final_file_name = str(pic_id) + "." + pic_format
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], final_file_name))
            db = extensions.connect_to_database()
            cur = db.cursor()
            cur.execute('USE maindb')
            cur.execute('SELECT picid FROM Photo WHERE picid = "%s"' % (pic_id))
            existing_pic = cur.fetchall()
            if not existing_pic:
                cur.execute('INSERT INTO Photo (picid, format, picDate) VALUES("%s", "%s", CURRENT_TIME())' % (pic_id, pic_format))
                cur.execute('SELECT * FROM Contain')
                max_seq = cur.fetchall()
                max_num = 0;
                for pics in max_seq:
                    if int(pics['sequencenum']) > max_num:
                        max_num = int(pics['sequencenum'])
                max_num = max_num + 1
                cur.execute('INSERT INTO Contain (sequencenum, albumid, picid, caption) VALUES(%d, %d, "%s", "%s")' % (max_num, album_id, pic_id, ""))
                cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
        elif op == "grant":
            username = request.form.get('username')
            cur.execute('SELECT * FROM User WHERE username = "%s"' % (username))
            name = cur.fetchall()
            if not name:
                abort(404)
            cur.execute('SELECT * FROM Album WHERE albumid = %d' % (album_id))
            album_exist = cur.fetchall()
            access = album_exist[0]['access']
            if access == "private":
                cur.execute('INSERT INTO AlbumAccess (albumid, username) VALUES (%d, "%s")' % (album_id, username))
            cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
        elif op =="revoke":
            username = request.form.get('username')
            cur.execute('SELECT * FROM User WHERE username = "%s"' % (username))
            name = cur.fetchall()
            if not name:
                abort(404)
            cur.execute('DELETE FROM AlbumAccess WHERE username = "%s"' % (username))
            cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
        elif op =="access":
            access = request.form.get('access')
            cur.execute('UPDATE Album SET lastupdated = CURRENT_TIME() WHERE albumid = "%s"' % (album_id))
            cur.execute('UPDATE Album SET access = "%s" WHERE albumid = "%s"' % (access, album_id))
            if access == "public":
                cur.execute('DELETE FROM AlbumAccess WHERE albumid = "%s"'% (album_id))

    return redirect(url_for('album.album_edit_route', albumid=album_id))

    
@album.route('/album')
def album_route():
    return render_template("album.html")




