from flask import Blueprint

utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')

@utilizador_blueprint.route('/')
def index():
    return 'Olá Turma'