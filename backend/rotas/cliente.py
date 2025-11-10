#rotas. Recebe as infos via api e chama o servico de cliente (servicos/cliente.py)

from flask import Blueprint, jsonify, request
from servicos.cliente import ClienteDatabase

cliente_blueprint = Blueprint("cliente", __name__)

# busca cliente via cpf
@cliente_blueprint.route("/cliente", methods=["GET"])
def get_clientes():
    cpf = request.args.get("cpf", "")
    return jsonify(ClienteDatabase().get_clientes(cpf)), 200

# cadastra cliente (cpf, nome, end)
@cliente_blueprint.route("/cliente", methods=["POST"])
def post_cliente():
    json = request.get_json()
    cpf = json.get("cpf")
    nome = json.get("nome")
    endereco = json.get("endereco")

    if not cpf or not nome:
        return jsonify("CPF e nome são obrigatórios"), 400

    result = ClienteDatabase().cadastra_cliente(cpf, nome, endereco)
    if result:
        return jsonify("Cliente cadastrado"), 200
    return jsonify("Erro ao cadastrar cliente"), 400

# atualiza nome, end do cliente
@cliente_blueprint.route("/cliente/<cpf>", methods=["PUT"])
def put_cliente(cpf):
    json = request.get_json()
    nome = json.get("nome")
    endereco = json.get("endereco")

    result = ClienteDatabase().atualiza_cliente(cpf, nome, endereco)
    if result:
        return jsonify("Cliente atualizado"), 200
    return jsonify("Erro ao atualizar cliente"), 400

@cliente_blueprint.route("/cliente/<cpf>", methods=["DELETE"])
def delete_cliente(cpf):
    result = ClienteDatabase().deleta_cliente(cpf)
    if result:
        return jsonify("Cliente deletado"), 200
    return jsonify("Erro ao deletar cliente"), 400

