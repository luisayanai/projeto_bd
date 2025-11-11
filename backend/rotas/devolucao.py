#rotas. Recebe as infos via api e chama o servico de devolucao (servicos/devolucao.py)

from flask import Blueprint, jsonify, request
from servicos.devolucao import DevolucaoDatabase

devolucao_blueprint = Blueprint("devolucao", __name__)

@devolucao_blueprint.route("/devolucao", methods=["GET"])
def get_devolucoes():
    id_devolucao = request.args.get("id_devolucao", "")
    id_venda = request.args.get("id_venda", "")
    cpf_cliente = request.args.get("cpf_cliente", "")
    
    id_devolucao_int = int(id_devolucao) if id_devolucao else None
    id_venda_int = int(id_venda) if id_venda else None
    return jsonify(DevolucaoDatabase().get_devolucoes(id_devolucao_int, id_venda_int, cpf_cliente)), 200

@devolucao_blueprint.route("/devolucao", methods=["POST"])
def post_devolucao():
    json = request.get_json()
    id_venda = json.get("id_venda")
    credito = json.get("credito")
    cpf_cliente = json.get("cpf_cliente")

    if not id_venda or credito is None or not cpf_cliente:
        return jsonify("ID da venda, crédito e CPF do cliente são obrigatórios"), 400

    result = DevolucaoDatabase().cadastra_devolucao(id_venda, credito, cpf_cliente)
    if result:
        return jsonify("Devolução cadastrada"), 200
    return jsonify("Erro ao cadastrar devolução"), 400



@devolucao_blueprint.route("/devolucao/<int:id_devolucao>", methods=["DELETE"])
def delete_devolucao(id_devolucao):
    result = DevolucaoDatabase().deleta_devolucao(id_devolucao)
    if result:
        return jsonify("Devolução deletada"), 200
    return jsonify("Erro ao deletar devolução"), 400

