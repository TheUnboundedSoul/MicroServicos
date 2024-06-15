from flask import Flask
from routes import encomenda_blueprint
from models import db, init_app
from flask_migrate import Migrate
app = Flask(__name__)
import os



app.config['SECRET_KEY'] = "chave"
file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'encomenda.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(encomenda_blueprint)
init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=5003)