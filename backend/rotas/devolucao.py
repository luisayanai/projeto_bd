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
    id_devolucao = json.get("id_devolucao")
    id_venda = json.get("id_venda")
    id_produto = json.get("id_produto")
    credito = json.get("credito")
    cpf_cliente = json.get("cpf_cliente")

    if not id_devolucao or not id_venda or id_produto is None or credito is None or not cpf_cliente:
        return jsonify("ID da devolução, ID da venda, ID do produto, crédito e CPF do cliente são obrigatórios"), 400

    try:
        id_devolucao_int = int(id_devolucao)
        id_venda_int = int(id_venda)
        id_produto_int = int(id_produto)
        credito_float = float(credito)
    except (TypeError, ValueError):
        return jsonify("IDs e crédito precisam ser numéricos"), 400

    result = DevolucaoDatabase().cadastra_devolucao(id_devolucao_int, id_venda_int, id_produto_int, credito_float, cpf_cliente)
    if result:
        return jsonify("Devolução cadastrada"), 200
    return jsonify("Erro ao cadastrar devolução"), 400



@devolucao_blueprint.route("/devolucao/<int:id_devolucao>", methods=["DELETE"])
def delete_devolucao(id_devolucao):
    result = DevolucaoDatabase().deleta_devolucao(id_devolucao)
    if result:
        return jsonify("Devolução deletada"), 200
    return jsonify("Erro ao deletar devolução"), 400

