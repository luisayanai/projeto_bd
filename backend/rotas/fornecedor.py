#rotas. Recebe as infos via api e chama o servico de fornecedor (servicos/fornecedor.py)

from flask import Blueprint, jsonify, request
from servicos.fornecedor import FornecedorDatabase

fornecedor_blueprint = Blueprint("fornecedor", __name__)

@fornecedor_blueprint.route("/fornecedor", methods=["GET"])
def get_fornecedores():
    cnpj = request.args.get("cnpj", "")
    id_produto = request.args.get("id_produto", "")
    
    id_produto_int = int(id_produto) if id_produto else None
    return jsonify(FornecedorDatabase().get_fornecedores(cnpj, id_produto_int)), 200

@fornecedor_blueprint.route("/fornecedor", methods=["POST"])
def post_fornecedor():
    json = request.get_json()
    cnpj = json.get("cnpj")
    nome = json.get("nome")
    id_produto = json.get("id_produto")
    preco = json.get("preco")
    telefone = json.get("telefone")
    email = json.get("email")

    if not cnpj or not nome or id_produto is None or preco is None:
        return jsonify("CNPJ, nome, ID do produto e preço são obrigatórios"), 400

    result = FornecedorDatabase().cadastra_fornecedor(cnpj, nome, id_produto, preco, telefone, email)
    if result:
        return jsonify("Fornecedor cadastrado"), 200
    return jsonify("Erro ao cadastrar fornecedor"), 400

@fornecedor_blueprint.route("/fornecedor/<cnpj>", methods=["PUT"])
def put_fornecedor(cnpj):
    json = request.get_json()
    nome = json.get("nome")
    telefone = json.get("telefone")
    email = json.get("email")
    id_produto = json.get("id_produto")
    preco = json.get("preco")

    result = FornecedorDatabase().atualiza_fornecedor(cnpj, nome, telefone, email, id_produto, preco)
    if result:
        return jsonify("Fornecedor atualizado"), 200
    return jsonify("Erro ao atualizar fornecedor"), 400

@fornecedor_blueprint.route("/fornecedor/<cnpj>", methods=["DELETE"])
def delete_fornecedor(cnpj):
    result = FornecedorDatabase().deleta_fornecedor(cnpj)
    if result:
        return jsonify("Fornecedor deletado"), 200
    return jsonify("Erro ao deletar fornecedor"), 400

