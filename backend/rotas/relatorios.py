#rotas. Recebe as infos via api e chama o servico de relatórios (servicos/relatorios.py)

from flask import Blueprint, jsonify, request
from servicos.relatorios import RelatoriosDatabase

relatorios_blueprint = Blueprint("relatorios", __name__)

@relatorios_blueprint.route("/relatorios/faturamento-mensal-filial", methods=["GET"])
def get_faturamento_mensal_filial():
    # query 1: faturamento mensal por filial
   
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)
        
    result = RelatoriosDatabase().faturamento_mensal_filial(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/top-clientes-mais-gastaram", methods=["GET"])
def get_top_clientes_mais_gastaram():
    # query 2: top N clientes que mais gastaram
    limite = request.args.get("limite", default=10, type=int)
    result = RelatoriosDatabase().top_clientes_mais_gastaram(limite)

    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/ticket-medio-fidelizado", methods=["GET"])
def get_ticket_medio_fidelizado():
    # query 3: valor médio gasto por clientes fidelizados e não fidelizados
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)

    result = RelatoriosDatabase().ticket_medio_fidelizado(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/ranking-funcionarios-vendas", methods=["GET"])
def get_ranking_funcionarios_vendas():
    # query 4: ranking de funcion?rios por vendas
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)

    if mes is not None and (mes < 1 or mes > 12):
        return jsonify("Mês deve estar entre 1 e 12"), 400
    if ano is not None and ano <= 0:
        return jsonify("Ano deve ser maior que zero"), 400

    result = RelatoriosDatabase().ranking_funcionarios_vendas(ano, mes)

    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-mais-vendidos", methods=["GET"])
def get_produtos_mais_vendidos():
    # query 5: produtos mais vendidos
    #quantidade_minima = request.args.get("quantidade_minima", default=50, type=int)

    result = RelatoriosDatabase().produtos_mais_vendidos()
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-maior-indice-devolucao", methods=["GET"])
def get_produtos_maior_indice_devolucao():
    # query 6: produtos com maior índice de devolução
    limite = request.args.get("limite", default=10, type=int)

    result = RelatoriosDatabase().produtos_maior_indice_devolucao(limite)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-estoque-abaixo-minimo", methods=["GET"])
def get_produtos_estoque_abaixo_minimo():
    # query 7: produtos com estoque abaixo do mínimo por filial
    endereco_filial = request.args.get("endereco_filial", default=None, type=str)

    result = RelatoriosDatabase().produtos_estoque_abaixo_minimo(endereco_filial)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/fornecedores-maior-volume-pedidos", methods=["GET"])
def get_fornecedores_maior_volume_pedidos():
    # query 8: fornecedores com maior volume e valor de pedidos
    limite = request.args.get("limite", default=10, type=int)
    
    result = RelatoriosDatabase().fornecedores_maior_volume_pedidos(limite)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/distribuicao-vendas-forma-pagamento", methods=["GET"])
def get_distribuicao_vendas_forma_pagamento():
    # query 9: distribuição de vendas por forma de pagamento
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)
    
    result = RelatoriosDatabase().distribuicao_vendas_forma_pagamento(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/clientes-gasto-acima-media", methods=["GET"])
def get_clientes_gasto_acima_media():
    # query 10: clientes com gasto acima da média dos total de clientes
    limite = request.args.get("limite", type=int)
    
    if limite is not None and limite <= 0:
        return jsonify("Limite deve ser maior que zero"), 400
    
    result = RelatoriosDatabase().clientes_gasto_acima_media(limite)
    return jsonify(result), 200

