from flask import Blueprint,jsonify, request,make_response
from models import db, Utilizador
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')

@utilizador_blueprint.route('/criar', methods=['POST'])
def criar_utilizador():
    try:
        # Verificação se o nomeUtilizador e apassword estao presentes
        nomeUtilizador = request.form.get
def index():
    return 'Olá Turma'