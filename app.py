from flask import Flask, render_template, session, redirect, url_for, escape, request
import extensions
import controllers
import api
import config

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')
app.secret_key='\xc2{\xe0m/\xc9\x8b\xe7 1\xdb\xf6\x86\xe4K\x85Z:\x96\x1e\xdaM_V'
# Register the controllers
app.register_blueprint(controllers.album, url_prefix='/p2gkisj6/p3')
app.register_blueprint(controllers.albums, url_prefix='/p2gkisj6/p3')
app.register_blueprint(controllers.pic, url_prefix='/p2gkisj6/p3')
app.register_blueprint(controllers.main, url_prefix='/p2gkisj6/p3')
app.register_blueprint(api.user, url_prefix='/p2gkisj6/p3')

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
