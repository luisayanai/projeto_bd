# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class ProdutoDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_produtos(self, id_produto: int = None, endereco_filial: str = None, categoria: str = None):
        query = "SELECT * FROM produto"
        conditions = []
        if id_produto:
            conditions.append(f"idproduto = {id_produto}")
        if endereco_filial:
            conditions.append(f"enderecofilial = '{endereco_filial}'")
        if categoria:
            conditions.append(f"categoria = '{categoria}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    
    def cadastra_produto(self, id_produto: int, categoria: str, cor: str, tamanho: str, preco_venda: float, endereco_filial: str, quant_min: str, quantidade: str):
        statement = f"INSERT INTO produto (idproduto, categoria, cor, tamanho, precovenda, enderecofilial, quant_min, quantidade) VALUES ({id_produto}, '{categoria}', '{cor}', '{tamanho}', {preco_venda}, '{endereco_filial}', '{quant_min}', '{quantidade}')"
        
        return self.db.execute_statement(statement)

    def atualiza_produto(self, id_produto: int, categoria: str = None, cor: str = None, tamanho: str = None, preco_venda: float = None, endereco_filial: str = None, quant_min: str = None, quantidade: str = None):
        updates = []
        if categoria:
            updates.append(f"categoria = '{categoria}'")
        if cor:
            updates.append(f"cor = '{cor}'")
        if tamanho:
            updates.append(f"tamanho = '{tamanho}'")
        if preco_venda is not None:
            updates.append(f"precovenda = {preco_venda}")
        if endereco_filial:
            updates.append(f"enderecofilial = '{endereco_filial}'")
        if quant_min:
            updates.append(f"quant_min = '{quant_min}'")
        if quantidade:
            updates.append(f"quantidade = '{quantidade}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE produto SET {', '.join(updates)} WHERE idproduto = {id_produto}"
        return self.db.execute_statement(statement)

    def deleta_produto(self, id_produto: int):
        statement = f"DELETE FROM produto WHERE idproduto = {id_produto}"
        return self.db.execute_statement(statement)

