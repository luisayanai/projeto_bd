# faz consultas de relatórios no database

from servicos.database.conector import DatabaseManager

class RelatoriosDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # query 1
    def faturamento_mensal_filial(self, ano: int = None, mes: int = None):
        """
        Retorna o faturamento mensal por filial
            se ano não for fornecido, usa o ano atual
            se mes não for fornecido, retorna todos os meses do ano
        """
        if ano is None:
            query = """
            SELECT
                t.filial,
                EXTRACT(YEAR FROM t.data_compra) AS ano,
                EXTRACT(MONTH FROM t.data_compra) AS mes,
                SUM(t.valor_bruto) AS faturamento_bruto,
                SUM(t.desconto) AS descontos_totais,
                SUM(t.valor_liquido) AS faturamento_liquido
            FROM (
                SELECT
                    v.idvenda,
                    v.data_compra,
                    f.endereco AS filial,
                    SUM(iv.quantidade * p.preco_venda) AS valor_bruto,
                    v.valor_desconto AS desconto,
                    SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
                FROM venda v
                JOIN funcionario fun ON fun.cpf = v.cpf_funcionario
                JOIN filial f ON f.endereco = fun.endereco_filial
                JOIN item_venda iv ON iv.idvenda = v.idvenda
                JOIN produto p ON p.idproduto = iv.idproduto
                GROUP BY v.idvenda, v.data_compra, f.endereco, v.valor_desconto
            ) AS t
            WHERE EXTRACT(YEAR FROM t.data_compra) = EXTRACT(YEAR FROM CURRENT_DATE)
            GROUP BY t.filial, EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra)
            ORDER BY EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra), t.filial;
            """
        elif mes is None:
            query = f"""
            SELECT
                t.filial,
                EXTRACT(YEAR FROM t.data_compra) AS ano,
                EXTRACT(MONTH FROM t.data_compra) AS mes,
                SUM(t.valor_bruto) AS faturamento_bruto,
                SUM(t.desconto) AS descontos_totais,
                SUM(t.valor_liquido) AS faturamento_liquido
            FROM (
                SELECT
                    v.idvenda,
                    v.data_compra,
                    f.endereco AS filial,
                    SUM(iv.quantidade * p.preco_venda) AS valor_bruto,
                    v.valor_desconto AS desconto,
                    SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
                FROM venda v
                JOIN funcionario fun ON fun.cpf = v.cpf_funcionario
                JOIN filial f ON f.endereco = fun.endereco_filial
                JOIN item_venda iv ON iv.idvenda = v.idvenda
                JOIN produto p ON p.idproduto = iv.idproduto
                GROUP BY v.idvenda, v.data_compra, f.endereco, v.valor_desconto
            ) AS t
            WHERE EXTRACT(YEAR FROM t.data_compra) = {ano}
            GROUP BY t.filial, EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra)
            ORDER BY EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra), t.filial;
            """
        else:
            query = f"""
            SELECT
                t.filial,
                EXTRACT(YEAR FROM t.data_compra) AS ano,
                EXTRACT(MONTH FROM t.data_compra) AS mes,
                SUM(t.valor_bruto) AS faturamento_bruto,
                SUM(t.desconto) AS descontos_totais,
                SUM(t.valor_liquido) AS faturamento_liquido
            FROM (
                SELECT
                    v.idvenda,
                    v.data_compra,
                    f.endereco AS filial,
                    SUM(iv.quantidade * p.preco_venda) AS valor_bruto,
                    v.valor_desconto AS desconto,
                    SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
                FROM venda v
                JOIN funcionario fun ON fun.cpf = v.cpf_funcionario
                JOIN filial f ON f.endereco = fun.endereco_filial
                JOIN item_venda iv ON iv.idvenda = v.idvenda
                JOIN produto p ON p.idproduto = iv.idproduto
                GROUP BY v.idvenda, v.data_compra, f.endereco, v.valor_desconto
            ) AS t
            WHERE EXTRACT(YEAR FROM t.data_compra) = {ano} AND EXTRACT(MONTH FROM t.data_compra) = {mes}
            GROUP BY t.filial, EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra)
            ORDER BY EXTRACT(YEAR FROM t.data_compra), EXTRACT(MONTH FROM t.data_compra), t.filial;
            """
        
        return self.db.execute_select_all(query)

    # query 2
    def top_clientes_mais_gastaram(self, limite: int = 10):
        """
        Retorna os N clientes que mais gastaram na loja
        """
        query = f"""
        SELECT
            c.cpf,
            c.nome,
            SUM(t.valor_liquido) AS total_gasto
        FROM (
            SELECT
                v.idvenda,
                v.cpf_cliente,
                SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
            FROM venda v
            JOIN item_venda iv ON iv.idvenda = v.idvenda
            JOIN produto p ON p.idproduto = iv.idproduto
            GROUP BY v.idvenda, v.cpf_cliente, v.valor_desconto
        ) AS t
        JOIN cliente c ON c.cpf = t.cpf_cliente
        GROUP BY c.cpf, c.nome
        ORDER BY total_gasto DESC
        LIMIT {limite};
        """
        return self.db.execute_select_all(query)

    # query 3
    def ticket_medio_fidelizado(self, ano: int = None, mes: int = None):
        """
        Compara o ticket médio entre clientes fidelizados e não fidelizados
            se ano não for fornecido, usa todos os dados
            se mes não for fornecido, usa todos os meses do ano
        """
        where_clause = ""
        if ano is not None and mes is not None:
            where_clause = f"WHERE EXTRACT(YEAR FROM v.data_compra) = {ano} AND EXTRACT(MONTH FROM v.data_compra) = {mes}"
        elif ano is not None:
            where_clause = f"WHERE EXTRACT(YEAR FROM v.data_compra) = {ano}"
        
        query = f"""
        SELECT
            (cf.cpfcliente IS NOT NULL) AS eh_fidelizado,
            (cf.cpfcliente IS NULL) AS nao_fidelizado,
            COUNT(t.idvenda) AS quantidade_vendas,
            SUM(t.valor_liquido) AS valor_total,
            AVG(t.valor_liquido) AS ticket_medio
        FROM (
            SELECT
                v.idvenda,
                v.cpf_cliente,
                v.data_compra,
                SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
            FROM venda v
            JOIN item_venda iv ON iv.idvenda = v.idvenda
            JOIN produto p ON p.idproduto = iv.idproduto
            {where_clause}
            GROUP BY v.idvenda, v.cpf_cliente, v.data_compra, v.valor_desconto
        ) AS t
        JOIN cliente c ON c.cpf = t.cpf_cliente
        LEFT JOIN cliente_fidelizado cf ON cf.cpfcliente = c.cpf
        GROUP BY eh_fidelizado, nao_fidelizado;
        """
        return self.db.execute_select_all(query)

    # query 4
    def ranking_funcionarios_vendas(self, meses: int = 1, valor_minimo: float = 5000.0):
        """
        Retorna funcionários com maior valor vendido nos últimos N meses (ostra apenas quem vendeu mais que valor_minimo)
        """
        query = f"""
        SELECT
            f.cpf,
            f.nome,
            COUNT(t.idvenda) AS quantidade_vendas,
            SUM(t.valor_liquido) AS valor_total_vendido
        FROM (
            SELECT
                v.idvenda,
                v.cpf_funcionario,
                v.data_compra,
                SUM(iv.quantidade * p.preco_venda) - v.valor_desconto AS valor_liquido
            FROM venda v
            JOIN item_venda iv ON iv.idvenda = v.idvenda
            JOIN produto p ON p.idproduto = iv.idproduto
            GROUP BY v.idvenda, v.cpf_funcionario, v.data_compra, v.valor_desconto
        ) AS t
        JOIN funcionario f ON f.cpf = t.cpf_funcionario
        WHERE t.data_compra >= CURRENT_DATE - INTERVAL '{meses} month'
        GROUP BY f.cpf, f.nome
        HAVING SUM(t.valor_liquido) > {valor_minimo}
        ORDER BY valor_total_vendido DESC;
        """
        return self.db.execute_select_all(query)

    # query 5
    def produtos_mais_vendidos(self, quantidade_minima: int = 50):
        """
        Retorna produtos com mais de quantidade_minima unidades vendidas
        """
        query = f"""
        SELECT
            p.idproduto,
            p.categoria,
            p.cor,
            p.tamanho,
            SUM(iv.quantidade) AS quantidade_vendida
        FROM produto p
        JOIN item_venda iv ON iv.idproduto = p.idproduto
        GROUP BY p.idproduto, p.categoria, p.cor, p.tamanho
        HAVING SUM(iv.quantidade) > {quantidade_minima}
        ORDER BY quantidade_vendida DESC;
        """
        return self.db.execute_select_all(query)

    # query 6
    def produtos_maior_indice_devolucao(self, limite: int = 10):
        """
        Retorna os N produtos com maior percentual de devolução
        """
        query = f"""
        SELECT
            p.idproduto,
            p.categoria,
            p.cor,
            p.tamanho,
            SUM(iv.quantidade) AS quantidade_vendida,
            COUNT(d.iddevolucao) AS quantidade_devolvida,
            (COUNT(d.iddevolucao) * 100.0 / NULLIF(SUM(iv.quantidade), 0)) AS percentual_devolucao
        FROM produto p
        JOIN item_venda iv ON iv.idproduto = p.idproduto
        LEFT JOIN devolucao d ON d.idproduto = p.idproduto
        GROUP BY p.idproduto, p.categoria, p.cor, p.tamanho
        HAVING SUM(iv.quantidade) > 0
        ORDER BY percentual_devolucao DESC
        LIMIT {limite};
        """
        return self.db.execute_select_all(query)

    # query 7
    def produtos_estoque_abaixo_minimo(self, endereco_filial: str = None):
        """
        Retorna produtos cujo estoque está abaixo do mínimo
            se endereco_filial foi dado, filtra por filial específica
        """
        if endereco_filial:
            query = f"""
            SELECT
                f.endereco AS filial,
                p.idproduto,
                p.categoria,
                p.cor,
                p.tamanho,
                p.quantidade AS quantidade_atual,
                p.quant_min AS quantidade_minima
            FROM produto p
            JOIN filial f ON f.endereco = p.endereco_filial
            WHERE p.quantidade < p.quant_min AND f.endereco = '{endereco_filial}'
            ORDER BY filial, p.categoria, p.idproduto;
            """
        else:
            query = """
            SELECT
                f.endereco AS filial,
                p.idproduto,
                p.categoria,
                p.cor,
                p.tamanho,
                p.quantidade AS quantidade_atual,
                p.quant_min AS quantidade_minima
            FROM produto p
            JOIN filial f ON f.endereco = p.endereco_filial
            WHERE p.quantidade < p.quant_min
            ORDER BY filial, p.categoria, p.idproduto;
            """
        return self.db.execute_select_all(query)

    # query 8
    def fornecedores_maior_volume_pedidos(self, limite: int = 10):
        """
        Retorna os N fornecedores com maior quantidade e valor de pedidos
        """
        query = f"""
        SELECT
            f.cnpj,
            f.nome,
            SUM(ped.quantidade) AS quantidade_total_pedida,
            SUM(ped.quantidade * p.preco_venda) AS valor_estimado
        FROM pedido ped
        JOIN fornecedor f ON f.cnpj = ped.cnpj_fornec
        JOIN produto p ON p.idproduto = ped.idproduto
        GROUP BY f.cnpj, f.nome
        ORDER BY valor_estimado DESC
        LIMIT {limite};
        """
        return self.db.execute_select_all(query)

    # query 9
    def distribuicao_vendas_forma_pagamento(self, ano: int = None, mes: int = None):
        """
        Retorna distribuição das vendas por forma de pagamento
            se ano não for fornecido, usa todos os dados
            se mes não for fornecido, usa todos os meses do ano
        """
        where_clause = "WHERE v.forma_pag IS NOT NULL"
        if ano is not None and mes is not None:
            where_clause = f"WHERE v.forma_pag IS NOT NULL AND EXTRACT(YEAR FROM v.data_compra) = {ano} AND EXTRACT(MONTH FROM v.data_compra) = {mes}"
        elif ano is not None:
            where_clause = f"WHERE v.forma_pag IS NOT NULL AND EXTRACT(YEAR FROM v.data_compra) = {ano}"
        
        query = f"""
        SELECT
            v.forma_pag,
            COUNT(DISTINCT v.idvenda) AS quantidade_vendas,
            SUM(iv.quantidade * p.preco_venda) - SUM(v.valor_desconto) AS valor_total,
            (SUM(iv.quantidade * p.preco_venda) - SUM(v.valor_desconto)) 
                / NULLIF(COUNT(DISTINCT v.idvenda), 0) AS ticket_medio
        FROM venda v
        JOIN item_venda iv ON iv.idvenda = v.idvenda
        JOIN produto p ON p.idproduto = iv.idproduto
        {where_clause}
        GROUP BY v.forma_pag
        ORDER BY valor_total DESC;
        """
        return self.db.execute_select_all(query)

    # query 10
    def clientes_gasto_acima_media(self, limite: int = None):
        """
        Retorna os N clientes que gastaram acima da média, informando se são fidelizados
            se limite não for fornecido, retorna todos
        """
        limit_clause = f"LIMIT {limite}" if limite is not None else ""
        
        query = f"""
        SELECT
            c.cpf,
            c.nome,
            (cf.cpfcliente IS NOT NULL) AS eh_fidelizado,
            (cf.cpfcliente IS NULL) AS nao_fidelizado,
            gc.total_gasto
        FROM (
            SELECT
                v.cpf_cliente,
                SUM(iv.quantidade * p.preco_venda) - SUM(v.valor_desconto) AS total_gasto
            FROM venda v
            JOIN item_venda iv ON iv.idvenda = v.idvenda
            JOIN produto p ON p.idproduto = iv.idproduto
            GROUP BY v.cpf_cliente
        ) AS gc
        JOIN cliente c ON c.cpf = gc.cpf_cliente
        LEFT JOIN cliente_fidelizado cf ON cf.cpfcliente = c.cpf
        WHERE gc.total_gasto >
            (SELECT AVG(total_gasto)
             FROM (
                 SELECT
                     v.cpf_cliente,
                     SUM(iv.quantidade * p.preco_venda) - SUM(v.valor_desconto) AS total_gasto
                 FROM venda v
                 JOIN item_venda iv ON iv.idvenda = v.idvenda
                 JOIN produto p ON p.idproduto = iv.idproduto
                 GROUP BY v.cpf_cliente
             ) AS medias)
        ORDER BY gc.total_gasto DESC
        {limit_clause};
        """
        return self.db.execute_select_all(query)

