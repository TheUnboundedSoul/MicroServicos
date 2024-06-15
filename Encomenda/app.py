from flask import Flask
from routes import encomenda_blueprint
from models import db, init_app
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_ngYcYBFSa7U-7_aXkH-g'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
file_path = os.path.abspath(os.path.join(os.getcwd(), 'D:\\Faculdade\Mestrado\\2 Semestre\\Arquitetura de Software\\MicroServicos\\Encomenda\\database', 'encomenda.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

app.register_blueprint(encomenda_blueprint)
init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
