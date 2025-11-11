#rotas. Recebe as infos via api e chama o servico de cliente_fidelizado (servicos/cliente_fidelizado.py)

from flask import Blueprint, jsonify, request
from servicos.cliente_fidelizado import ClienteFidelizadoDatabase

cliente_fidelizado_blueprint = Blueprint("cliente_fidelizado", __name__)

@cliente_fidelizado_blueprint.route("/cliente_fidelizado", methods=["GET"])
def get_clientes_fidelizados():
    id_cadastro = request.args.get("id_cadastro", "")
    cpf_cliente = request.args.get("cpf_cliente", "")
    
    id_cadastro_int = int(id_cadastro) if id_cadastro else None
    return jsonify(ClienteFidelizadoDatabase().get_clientes_fidelizados(id_cadastro_int, cpf_cliente)), 200

@cliente_fidelizado_blueprint.route("/cliente_fidelizado", methods=["POST"])
def post_cliente_fidelizado():
    json = request.get_json()
    cpf_cliente = json.get("cpf_cliente")
    pontos = json.get("pontos")
    email = json.get("email")

    if not cpf_cliente:
        return jsonify("CPF do cliente é obrigatório"), 400

    result = ClienteFidelizadoDatabase().cadastra_cliente_fidelizado(cpf_cliente, pontos, email)
    if result:
        return jsonify("Cliente fidelizado cadastrado"), 200
    return jsonify("Erro ao cadastrar cliente fidelizado"), 400

# atualiza infos do cliente cadastrado
@cliente_fidelizado_blueprint.route("/cliente_fidelizado/<int:id_cadastro>", methods=["PUT"])
def put_cliente_fidelizado(id_cadastro):
    json = request.get_json()
    pontos = json.get("pontos")
    email = json.get("email")
    cpf_cliente = json.get("cpf_cliente")

    result = ClienteFidelizadoDatabase().atualiza_cliente_fidelizado(id_cadastro, pontos, email, cpf_cliente)
    if result:
        return jsonify("Cliente fidelizado atualizado"), 200
    return jsonify("Erro ao atualizar cliente fidelizado"), 400

@cliente_fidelizado_blueprint.route("/cliente_fidelizado/<int:id_cadastro>", methods=["DELETE"])
def delete_cliente_fidelizado(id_cadastro):
    result = ClienteFidelizadoDatabase().deleta_cliente_fidelizado(id_cadastro)
    if result:
        return jsonify("Cliente fidelizado deletado"), 200
    return jsonify("Erro ao deletar cliente fidelizado"), 400

