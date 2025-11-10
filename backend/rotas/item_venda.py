#rotas. Recebe as infos via api e chama o servico de item_venda (servicos/item_venda.py)

from flask import Blueprint, jsonify, request
from servicos.item_venda import ItemVendaDatabase

item_venda_blueprint = Blueprint("item_venda", __name__)

@item_venda_blueprint.route("/item_venda", methods=["GET"])
def get_itens_venda():
    id_venda = request.args.get("id_venda", "")
    id_produto = request.args.get("id_produto", "")
    
    id_venda_int = int(id_venda) if id_venda else None
    id_produto_int = int(id_produto) if id_produto else None
    return jsonify(ItemVendaDatabase().get_itens_venda(id_venda_int, id_produto_int)), 200

@item_venda_blueprint.route("/item_venda", methods=["POST"])
def post_item_venda():
    json = request.get_json()
    id_venda = json.get("id_venda")
    id_produto = json.get("id_produto")
    quantidade = json.get("quantidade")

    if not all([id_venda, id_produto, quantidade]):
        return jsonify("ID da venda, ID do produto e quantidade são obrigatórios"), 400

    result = ItemVendaDatabase().cadastra_item_venda(id_venda, id_produto, quantidade)
    if result:
        return jsonify("Item de venda cadastrado"), 200
    return jsonify("Erro ao cadastrar item de venda"), 400

@item_venda_blueprint.route("/item_venda/<int:id_venda>/<int:id_produto>", methods=["PUT"])
def put_item_venda(id_venda, id_produto):
    json = request.get_json()
    quantidade = json.get("quantidade")

    result = ItemVendaDatabase().atualiza_item_venda(id_venda, id_produto, quantidade)
    if result:
        return jsonify("Item de venda atualizado"), 200
    return jsonify("Erro ao atualizar item de venda"), 400

@item_venda_blueprint.route("/item_venda/<int:id_venda>/<int:id_produto>", methods=["DELETE"])
def delete_item_venda(id_venda, id_produto):
    result = ItemVendaDatabase().deleta_item_venda(id_venda, id_produto)
    if result:
        return jsonify("Item de venda deletado"), 200
    return jsonify("Erro ao deletar item de venda"), 400

