from flask import Flask, g, redirect, url_for
from flask.sessions import SecureCookieSessionInterface
from flask_migrate import Migrate
from flask_login import LoginManager
import models
from Utilizador.routes import utilizador_blueprint
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'v7K7siKrV8BL46KsyAIPoQ'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'utilizador.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)
app.register_blueprint(utilizador_blueprint)

login_manager = LoginManager(app)
migrate = Migrate(app, models.db)

@login_manager.user_loader
def load_user(utilizadorId):
    return models.Utilizador.query.filter_by(id=utilizadorId).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        utilizador = models.Utilizador.query.filter_by(api_key=api_key).first()
        if utilizador:
            return utilizador

class CustomSessionInterface(SecureCookieSessionInterface):
    """ Impedir a criação de sessões a partir de solicitações da API """
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

@app.route('/')
def home():
    return redirect(url_for('utilizador_api_routes.index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
