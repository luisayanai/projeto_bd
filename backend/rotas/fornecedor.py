#rotas. Recebe as infos via api e chama o servico de fornecedor (servicos/fornecedor.py)

from flask import Blueprint, jsonify, request
from servicos.fornecedor import FornecedorDatabase

fornecedor_blueprint = Blueprint("fornecedor", __name__)

@fornecedor_blueprint.route("/fornecedor", methods=["GET"])
def get_fornecedores():
    cnpj = request.args.get("cnpj", "")
    nome = request.args.get("nome", "")
    
    return jsonify(FornecedorDatabase().get_fornecedores(cnpj, nome)), 200

@fornecedor_blueprint.route("/fornecedor", methods=["POST"])
def post_fornecedor():
    json = request.get_json()
    cnpj = json.get("cnpj")
    nome = json.get("nome")
    telefone = json.get("telefone")
    email = json.get("email")

    if not cnpj or not nome:
        return jsonify("CNPJ e nome são obrigatórios"), 400

    result = FornecedorDatabase().cadastra_fornecedor(cnpj, nome, telefone, email)
    if result:
        return jsonify("Fornecedor cadastrado"), 200
    return jsonify("Erro ao cadastrar fornecedor"), 400

@fornecedor_blueprint.route("/fornecedor/<cnpj>", methods=["DELETE"])
def delete_fornecedor(cnpj):
    result = FornecedorDatabase().deleta_fornecedor(cnpj)
    if result:
        return jsonify("Fornecedor deletado"), 200
    return jsonify("Erro ao deletar fornecedor"), 400

