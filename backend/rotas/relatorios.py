#rotas. Recebe as infos via api e chama o servico de relatórios (servicos/relatorios.py)

from flask import Blueprint, jsonify, request
from servicos.relatorios import RelatoriosDatabase

relatorios_blueprint = Blueprint("relatorios", __name__)

@relatorios_blueprint.route("/relatorios/faturamento-mensal-filial", methods=["GET"])
def get_faturamento_mensal_filial():
    """
    Query 1: Faturamento mensal por filial
    Parâmetros opcionais: ano, mes
    """
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)
    
    result = RelatoriosDatabase().faturamento_mensal_filial(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/top-clientes-mais-gastaram", methods=["GET"])
def get_top_clientes_mais_gastaram():
    """
    Query 2: Top N clientes que mais gastaram
    Parâmetro opcional: limite (padrão: 10)
    """
    limite = request.args.get("limite", default=10, type=int)
    
    if limite <= 0:
        return jsonify("Limite deve ser maior que zero"), 400
    
    result = RelatoriosDatabase().top_clientes_mais_gastaram(limite)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/ticket-medio-fidelizado", methods=["GET"])
def get_ticket_medio_fidelizado():
    """
    Query 3: Valor médio gasto por clientes fidelizados e não fidelizados
    Parâmetros opcionais: ano, mes
    """
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)
    
    result = RelatoriosDatabase().ticket_medio_fidelizado(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/ranking-funcionarios-vendas", methods=["GET"])
def get_ranking_funcionarios_vendas():
    """
    Query 4: Ranking de funcionários por vendas
    Parâmetros opcionais: meses (padrão: 1), valor_minimo (padrão: 5000.0)
    """
    meses = request.args.get("meses", default=1, type=int)
    valor_minimo = request.args.get("valor_minimo", default=5000.0, type=float)
    
    if meses <= 0:
        return jsonify("Meses deve ser maior que zero"), 400
    if valor_minimo < 0:
        return jsonify("Valor mínimo deve ser maior ou igual a zero"), 400
    
    result = RelatoriosDatabase().ranking_funcionarios_vendas(meses, valor_minimo)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-mais-vendidos", methods=["GET"])
def get_produtos_mais_vendidos():
    """
    Query 5: Produtos mais vendidos
    Parâmetro opcional: quantidade_minima (padrão: 50)
    """
    quantidade_minima = request.args.get("quantidade_minima", default=50, type=int)
    
    if quantidade_minima < 0:
        return jsonify("Quantidade mínima deve ser maior ou igual a zero"), 400
    
    result = RelatoriosDatabase().produtos_mais_vendidos(quantidade_minima)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-maior-indice-devolucao", methods=["GET"])
def get_produtos_maior_indice_devolucao():
    """
    Query 6: Produtos com maior índice de devolução
    Parâmetro opcional: limite (padrão: 10)
    """
    limite = request.args.get("limite", default=10, type=int)
    
    if limite <= 0:
        return jsonify("Limite deve ser maior que zero"), 400
    
    result = RelatoriosDatabase().produtos_maior_indice_devolucao(limite)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/produtos-estoque-abaixo-minimo", methods=["GET"])
def get_produtos_estoque_abaixo_minimo():
    """
    Query 7: Produtos com estoque abaixo do mínimo por filial
    Parâmetro opcional: endereco_filial
    """
    endereco_filial = request.args.get("endereco_filial", default=None, type=str)
    
    result = RelatoriosDatabase().produtos_estoque_abaixo_minimo(endereco_filial)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/fornecedores-maior-volume-pedidos", methods=["GET"])
def get_fornecedores_maior_volume_pedidos():
    """
    Query 8: Fornecedores com maior volume e valor de pedidos
    Parâmetro opcional: limite (padrão: 10)
    """
    limite = request.args.get("limite", default=10, type=int)
    
    if limite <= 0:
        return jsonify("Limite deve ser maior que zero"), 400
    
    result = RelatoriosDatabase().fornecedores_maior_volume_pedidos(limite)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/distribuicao-vendas-forma-pagamento", methods=["GET"])
def get_distribuicao_vendas_forma_pagamento():
    """
    Query 9: Distribuição das vendas por forma de pagamento
    Parâmetros opcionais: ano, mes
    """
    ano = request.args.get("ano", type=int)
    mes = request.args.get("mes", type=int)
    
    result = RelatoriosDatabase().distribuicao_vendas_forma_pagamento(ano, mes)
    return jsonify(result), 200

@relatorios_blueprint.route("/relatorios/clientes-gasto-acima-media", methods=["GET"])
def get_clientes_gasto_acima_media():
    """
    Query 10: Clientes com gasto acima da média dos clientes
    Parâmetro opcional: limite (se não fornecido, retorna todos)
    """
    limite = request.args.get("limite", type=int)
    
    if limite is not None and limite <= 0:
        return jsonify("Limite deve ser maior que zero"), 400
    
    result = RelatoriosDatabase().clientes_gasto_acima_media(limite)
    return jsonify(result), 200

