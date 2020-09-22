from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from models import db

from log_req import logined


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from api import bp as api_bp


@app.route('/')
@logined
def game():
	return render_template('index.html', name = session.get('username'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':

		name = request.json.get('name')
		session['log'] = True
		session['username'] = name
	return render_template('login.html')

app.register_blueprint(api_bp, url_prefix = '/api')


if __name__ == '__main__':
	app.run(debug = True, port=4000)