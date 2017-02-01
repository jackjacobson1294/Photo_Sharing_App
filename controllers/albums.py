from flask import *
import extensions
import os, sys

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums/edit', methods=['POST', 'GET'])
def albums_edit_route():
    db = extensions.connect_to_database()
    cur = db.cursor()
    logged_in = False
    if 'username' in session:
        logged_in = True
    if logged_in:
        user = session['username']
    else:
        return redirect(url_for('main.login_route'))
    cur.execute('use maindb')
    cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
    user_exist = cur.fetchall()
    if not user_exist:
        abort(404)
    op = request.form.get('op')
    if not op:
        cur.execute('SELECT * FROM Album WHERE username = "%s"' % (user))
        albums = cur.fetchall()
        cur.execute('SELECT * FROM AlbumAccess WHERE username = "%s"' % (user))
        access_albums = cur.fetchall()
        cur.execute('SELECT * FROM Album')
        all_albums = cur.fetchall()
        options = {
            "access_albums": access_albums,
            "edit": True,
            "username": user,
            "albums": albums,
            "all_albums": all_albums
        }
        return render_template("albums.html", **options)

    elif op == "delete":
        album_id = int(request.form.get('albumid'))
        cur.execute('SELECT * FROM Contain WHERE albumid = %d' % (album_id))
        picids = cur.fetchall()
        cur.execute('DELETE FROM Contain WHERE albumid = %d' % (album_id))
        for pic in picids:
            cur.execute('SELECT format FROM Photo WHERE picid = "%s"' % pic['picid'])
            format = cur.fetchall()[0]['format']
            cur.execute('DELETE FROM Photo WHERE picid = "%s"' % pic['picid'])
            os.remove('/static/images/' + pic['picid'] + "." + str(format) )
        cur.execute('DELETE FROM Album WHERE albumid = %d' % (album_id))
        cur.execute('DELETE FROM AlbumAccess WHERE albumid = %d' % (album_id))
    else:
        title = request.form.get('title')
        cur.execute('INSERT INTO Album VALUES(NULL, "%s", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), "%s", "%s")' % (title, user, "private"))

    return redirect(url_for('albums.albums_edit_route', username=user))



@albums.route('/albums')
def albums_route():
    logged_in = False
    user = request.args.get('username')
    if not user:
        if 'username' in session:
            logged_in = True
        if logged_in:
            user = session['username']
        else:
            return redirect(url_for('main.login_route'))
    db = extensions.connect_to_database()
    cur = db.cursor()
    cur.execute('use maindb')
    cur.execute('SELECT * FROM User WHERE username = "%s"' % (user))
    user_exist = cur.fetchall()
    if not user_exist:
        abort(404)
    cur.execute('SELECT * FROM Album WHERE username = "%s"' % (user))
    albums = cur.fetchall()
    if logged_in:
        cur.execute('SELECT * FROM AlbumAccess WHERE username = "%s"' % (user))
        access_albums = cur.fetchall()

        options = {
            "access_albums": access_albums,
            "edit": False,
            "logged_in": logged_in,
            "username": user,
            "albums": albums
        }
        return render_template("albums.html", **options)
    
    else:
        cur.execute('SELECT * FROM Album WHERE username = "%s" and access = "%s"' % (user, "public"))
        public_albums = cur.fetchall()
        
        options = {
            "edit": False,
            "logged_in": logged_in,
            "username": user,
            "albums": albums,
            "public_albums": public_albums
        }
        
        return render_template("albums.html", **options)





