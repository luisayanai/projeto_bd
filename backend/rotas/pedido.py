#rotas. Recebe as infos via api e chama o servico de pedido (servicos/pedido.py)

from flask import Blueprint, jsonify, request
from servicos.pedido import PedidoDatabase

pedido_blueprint = Blueprint("pedido", __name__)

@pedido_blueprint.route("/pedido", methods=["GET"])
def get_pedidos():
    endereco_filial = request.args.get("endereco_filial", "")
    cnpj_fornec = request.args.get("cnpj_fornec", "")
    id_produto = request.args.get("id_produto", "")
    
    id_produto_int = int(id_produto) if id_produto else None
    return jsonify(PedidoDatabase().get_pedidos(endereco_filial, cnpj_fornec, id_produto_int)), 200

@pedido_blueprint.route("/pedido", methods=["POST"])
def post_pedido():
    json = request.get_json()
    endereco_filial = json.get("endereco_filial")
    cnpj_fornec = json.get("cnpj_fornec")
    id_produto = json.get("id_produto")
    data_pedido = json.get("data_pedido")
    quantidade = json.get("quantidade")

    if not all([endereco_filial, cnpj_fornec, id_produto, data_pedido, quantidade]):
        return jsonify("Endereço da filial, CNPJ do fornecedor, ID do produto, data do pedido e quantidade são obrigatórios"), 400

    result = PedidoDatabase().cadastra_pedido(endereco_filial, cnpj_fornec, id_produto, data_pedido, quantidade)
    if result:
        return jsonify("Pedido cadastrado"), 200
    return jsonify("Erro ao cadastrar pedido"), 400

@pedido_blueprint.route("/pedido", methods=["PUT"])
def put_pedido():
    json = request.get_json()
    endereco_filial = json.get("endereco_filial")
    cnpj_fornec = json.get("cnpj_fornec")
    id_produto = json.get("id_produto")
    data_pedido = json.get("data_pedido")
    quantidade = json.get("quantidade")

    result = PedidoDatabase().atualiza_pedido(endereco_filial, cnpj_fornec, id_produto, data_pedido, quantidade)
    if result:
        return jsonify("Pedido atualizado"), 200
    return jsonify("Erro ao atualizar pedido"), 400

@pedido_blueprint.route("/pedido", methods=["DELETE"])
def delete_pedido():
    json = request.get_json()
    endereco_filial = json.get("endereco_filial")
    cnpj_fornec = json.get("cnpj_fornec")
    id_produto = json.get("id_produto")

    result = PedidoDatabase().deleta_pedido(endereco_filial, cnpj_fornec, id_produto)
    if result:
        return jsonify("Pedido deletado"), 200
    return jsonify("Erro ao deletar pedido"), 400

