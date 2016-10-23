from flask import *
import extensions
import re
import uuid
import hashlib

logout = Blueprint('logout', __name__, template_folder='templates')

@logout.route("/api/v1/logout", methods=['POST'])
def user_logout():
	if 'username' in session:
		session.pop('username', None)
		session.pop('firstname', None)
		session.pop('lastname', None)
		return jsonify({}),204
	else:
		errors = []
		errors.append({'message':'You do not have the necessary credentials for the resource'})
		return jsonify(errors = errors), 401