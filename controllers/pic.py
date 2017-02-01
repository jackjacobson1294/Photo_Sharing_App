from flask import *
import extensions

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET','POST'])
def pic_route():
		return render_template("album.html")	





