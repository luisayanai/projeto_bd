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
    id_produto = json.get("id_produto")
    categoria = json.get("categoria")
    cor = json.get("cor")
    tamanho = json.get("tamanho")
    preco_venda = json.get("preco_venda")
    endereco_filial = json.get("endereco_filial")
    cnpj_fornecedor = json.get("cnpj_fornecedor")
    quant_min = json.get("quant_min")
    quantidade = json.get("quantidade")
    preco_compra = json.get("preco_compra")

    if not all([id_produto, categoria, cor, tamanho, preco_venda, endereco_filial, cnpj_fornecedor, quant_min, quantidade, preco_compra]):
        return jsonify("ID do produto, categoria, cor, tamanho, preços (venda e compra), endereço da filial, CNPJ do fornecedor, quantidade mínima e quantidade são obrigatórios"), 400

    try:
        id_produto_int = int(id_produto)
        quant_min_int = int(quant_min)
        quantidade_int = int(quantidade)
        preco_venda_float = float(preco_venda)
        preco_compra_float = float(preco_compra)
    except (TypeError, ValueError):
        return jsonify("ID do produto, quantidades e preços precisam ser numéricos"), 400

    result = ProdutoDatabase().cadastra_produto(
        id_produto_int,
        categoria,
        cor,
        tamanho,
        preco_venda_float,
        endereco_filial,
        cnpj_fornecedor,
        quant_min_int,
        quantidade_int,
        preco_compra_float,
    )
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
    cnpj_fornecedor = json.get("cnpj_fornecedor")
    quant_min = json.get("quant_min")
    quantidade = json.get("quantidade")
    preco_compra = json.get("preco_compra")

    try:
        preco_venda_float = float(preco_venda) if preco_venda is not None else None
        quant_min_int = int(quant_min) if quant_min is not None else None
        quantidade_int = int(quantidade) if quantidade is not None else None
        preco_compra_float = float(preco_compra) if preco_compra is not None else None
    except (TypeError, ValueError):
        return jsonify("Preços e quantidades precisam ser numéricos"), 400

    result = ProdutoDatabase().atualiza_produto(
        id_produto,
        categoria,
        cor,
        tamanho,
        preco_venda_float,
        endereco_filial,
        cnpj_fornecedor,
        quant_min_int,
        quantidade_int,
        preco_compra_float,
    )
    if result:
        return jsonify("Produto atualizado"), 200
    return jsonify("Erro ao atualizar produto"), 400

@produto_blueprint.route("/produto/<int:id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    result = ProdutoDatabase().deleta_produto(id_produto)
    if result:
        return jsonify("Produto deletado"), 200
    return jsonify("Erro ao deletar produto"), 400

