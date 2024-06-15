from flask import Blueprint, jsonify, request
from models import Encomenda, EncomendaLinha, db
import requests

encomenda_blueprint = Blueprint('encomenda_api_routes', __name__, url_prefix='/api/encomenda')

UTILIZADOR_API_URL = 'http://127.0.0.1:5001/api/utilizador'


def get_utilizador(api_key):
    headers = {
        'Authorization': api_key
    }
    response = requests.get(UTILIZADOR_API_URL, headers=headers)

    if response.status_code != 200:
        return {'message': 'Não autorizado 2.'}

    utilizador = response.json()
    return utilizador


@encomenda_blueprint.route('/', methods=['GET'])
def get_encomenda_pendente():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401

    encomendaPendente = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=1).first()

    if encomendaPendente:
        return jsonify({'result': encomendaPendente.serializar()}), 200
    else:
        return jsonify({'message': 'Sem encomenda pendente.'})


@encomenda_blueprint.route('/all', methods=['GET'])
def get_todas_encomendas():
    encomendas = Encomenda.query.all()
    result = [encomenda.serializar() for encomenda in encomendas]
    return jsonify(result), 200


@encomenda_blueprint.route('/adicionarArtigo', methods=['POST'])
def adicionar_item_encomenda():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado 0.'}), 401
    response = get_utilizador(api_key)
    if not response.get('result'):
        return jsonify({'message': 'Não está autenticado 1.'}), 401
    utilizador = response.get('result')
    artigoId = int(request.form['artigoId'])
    quantidade = int(request.form['quantidade'])
    utilizadorId = utilizador['id']

    encomendaPendente = Encomenda.query.filter_by(utilizadorId=utilizadorId, aberta=1).first()

    if not encomendaPendente:
        encomendaPendente = Encomenda()
        encomendaPendente.aberta = True
        encomendaPendente.utilizadorId = utilizadorId

        linhaEncomenda = EncomendaLinha(artigoId=artigoId, quantidade=quantidade)
        encomendaPendente.linhas_encomenda.append(linhaEncomenda)
    else:
        encontrou = False
        for linha in encomendaPendente.linhas_encomenda:
            if linha.artigoId == artigoId:
                linha.quantidade += quantidade
                encontrou = True
        if not encontrou:
            linhaEncomenda = EncomendaLinha(artigoId=artigoId, quantidade=quantidade)
            encomendaPendente.linha_encomenda.append(linhaEncomenda)
    db.session.add(encomendaPendente)
    db.session.commit()

    return jsonify({'result': encomendaPendente.serializar()})


@encomenda_blueprint.route('/checkout/', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401

    encomendaPendente = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=1).first()

    if encomendaPendente:
        encomendaPendente.aberta = False

        db.session.add(encomendaPendente)
        db.session.commit()
        return jsonify({'result': encomendaPendente.serializar()})
    else:
        return jsonify({'message': 'Sem encomenda pendente.'})


@encomenda_blueprint.route('/historico', methods=['GET'])
def historico_encomendas():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Não está autenticado.'}), 401
    response = get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message': 'Não está autenticado.'}), 401
    
    encomendas = Encomenda.query.filter_by(utilizadorId=utilizador['id'], aberta=False).all()
    result = [encomenda.serializar() for encomenda in encomendas]
    return jsonify(result), 200