#rotas. Recebe as infos via api e chama o servico de produto (servicos/produto.py)

from flask import Blueprint, jsonify, request
from servicos.produto import ProdutoDatabase

produto_blueprint = Blueprint("produto", __name__)

@produto_blueprint.route("/produto", methods=["GET"])
def get_produtos():
    id_produto = request.args.get("id_produto", "")
    endereco_filial = request.args.get("endereco_filial", "")
    categoria = request.args.get("categoria", "")
    
    id_produto_int = int(id_produto) if id_produto else None
    return jsonify(ProdutoDatabase().get_produtos(id_produto_int, endereco_filial, categoria)), 200

@produto_blueprint.route("/produto", methods=["POST"])
def post_produto():
    json = request.get_json()
    categoria = json.get("categoria")
    cor = json.get("cor")
    tamanho = json.get("tamanho")
    preco_venda = json.get("preco_venda")
    endereco_filial = json.get("endereco_filial")
    quant_min = json.get("quant_min")
    quantidade = json.get("quantidade")

    if not all([categoria, cor, tamanho, preco_venda, endereco_filial, quant_min, quantidade]):
        return jsonify("Categoria, cor, tamanho, preço de venda, endereço da filial, quantidade mínima e quantidade são obrigatórios"), 400

    result = ProdutoDatabase().cadastra_produto(categoria, cor, tamanho, preco_venda, endereco_filial, quant_min, quantidade)
    if result:
        return jsonify("Produto cadastrado"), 200
    return jsonify("Erro ao cadastrar produto"), 400

@produto_blueprint.route("/produto/<int:id_produto>", methods=["PUT"])
def put_produto(id_produto):
    json = request.get_json()
    categoria = json.get("categoria")
    cor = json.get("cor")
    tamanho = json.get("tamanho")
    preco_venda = json.get("preco_venda")
    endereco_filial = json.get("endereco_filial")
    quant_min = json.get("quant_min")
    quantidade = json.get("quantidade")

    result = ProdutoDatabase().atualiza_produto(id_produto, categoria, cor, tamanho, preco_venda, endereco_filial, quant_min, quantidade)
    if result:
        return jsonify("Produto atualizado"), 200
    return jsonify("Erro ao atualizar produto"), 400

@produto_blueprint.route("/produto/<int:id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    result = ProdutoDatabase().deleta_produto(id_produto)
    if result:
        return jsonify("Produto deletado"), 200
    return jsonify("Erro ao deletar produto"), 400

