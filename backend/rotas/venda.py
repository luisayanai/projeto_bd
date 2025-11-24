#rotas. Recebe as infos via api e chama o servico de venda (servicos/venda.py)

from flask import Blueprint, jsonify, request
from servicos.venda import VendaDatabase

venda_blueprint = Blueprint("venda", __name__)

@venda_blueprint.route("/venda", methods=["GET"])
def get_vendas():
    id_venda = request.args.get("id_venda", "")
    cpf_funcionario = request.args.get("cpf_funcionario", "")
    cpf_cliente = request.args.get("cpf_cliente", "")
    
    id_venda_int = int(id_venda) if id_venda else None
    return jsonify(VendaDatabase().get_vendas(id_venda_int, cpf_funcionario, cpf_cliente)), 200

@venda_blueprint.route("/venda", methods=["POST"])
def post_venda():
    json = request.get_json()
    id_venda = json.get("id_venda")
    data_compra = json.get("data_compra")
    status = json.get("status")
    valor_desconto = json.get("valor_desconto")
    cpf_funcionario = json.get("cpf_funcionario")
    cpf_cliente = json.get("cpf_cliente")
    comissao = json.get("comissao")
    forma_pag = json.get("forma_pag")
    parcelas = json.get("parcelas")

    if not id_venda or not data_compra or not status or valor_desconto is None or not cpf_funcionario or not cpf_cliente or comissao is None:
        return jsonify("ID da venda, data da compra, status, valor do desconto, CPF do funcionário, CPF do cliente e comissão são obrigatórios"), 400

    try:
        id_venda_int = int(id_venda)
        valor_desconto_float = float(valor_desconto)
        comissao_float = float(comissao)
        parcelas_int = int(parcelas) if parcelas is not None else None
    except (TypeError, ValueError):
        return jsonify("ID da venda, valor do desconto, comissão e parcelas precisam ser numéricos"), 400

    result = VendaDatabase().cadastra_venda(id_venda_int, data_compra, status, valor_desconto_float, cpf_funcionario, cpf_cliente, comissao_float, forma_pag, parcelas_int)
    if result:
        return jsonify("Venda cadastrada"), 200
    return jsonify("Erro ao cadastrar venda"), 400

@venda_blueprint.route("/venda/<int:id_venda>", methods=["PUT"])
def put_venda(id_venda):
    json = request.get_json()
    data_compra = json.get("data_compra")
    status = json.get("status")
    valor_desconto = json.get("valor_desconto")
    cpf_funcionario = json.get("cpf_funcionario")
    cpf_cliente = json.get("cpf_cliente")
    comissao = json.get("comissao")
    forma_pag = json.get("forma_pag")
    parcelas = json.get("parcelas")

    try:
        valor_desconto_float = float(valor_desconto) if valor_desconto is not None else None
        comissao_float = float(comissao) if comissao is not None else None
        parcelas_int = int(parcelas) if parcelas is not None else None
    except (TypeError, ValueError):
        return jsonify("Valores de desconto, comissão e parcelas precisam ser numéricos"), 400

    result = VendaDatabase().atualiza_venda(id_venda, data_compra, status, valor_desconto_float, cpf_funcionario, cpf_cliente, comissao_float, forma_pag, parcelas_int)
    if result:
        return jsonify("Venda atualizada"), 200
    return jsonify("Erro ao atualizar venda"), 400

@venda_blueprint.route("/venda/<int:id_venda>", methods=["DELETE"])
def delete_venda(id_venda):
    result = VendaDatabase().deleta_venda(id_venda)
    if result:
        return jsonify("Venda deletada"), 200
    return jsonify("Erro ao deletar venda"), 400

