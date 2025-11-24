# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class PedidoDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_pedidos(self, endereco_filial: str = None, cnpj_fornec: str = None, id_produto: int = None):
        query = "SELECT * FROM pedido"
        conditions = []
        if endereco_filial:
            conditions.append(f"endereco_filial = '{endereco_filial}'")
        if cnpj_fornec:
            conditions.append(f"cnpj_fornec = '{cnpj_fornec}'")
        if id_produto:
            conditions.append(f"idproduto = {id_produto}")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_pedido(self, endereco_filial: str, cnpj_fornec: str, id_produto: int):
        query = f"SELECT * FROM pedido WHERE endereco_filial = '{endereco_filial}' AND cnpj_fornec = '{cnpj_fornec}' AND idproduto = {id_produto}"
        return self.db.execute_select_one(query)
    
    def cadastra_pedido(self, endereco_filial: str, cnpj_fornec: str, id_produto: int, data_pedido: str, quantidade: str):
        statement = f"INSERT INTO pedido (endereco_filial, cnpj_fornec, idproduto, data_pedido, quantidade) VALUES ('{endereco_filial}', '{cnpj_fornec}', {id_produto}, '{data_pedido}', '{quantidade}')"
        
        return self.db.execute_statement(statement)

    def atualiza_pedido(self, endereco_filial: str, cnpj_fornec: str, id_produto: int, data_pedido: str = None, quantidade: str = None):
        updates = []
        if data_pedido:
            updates.append(f"data_pedido = '{data_pedido}'")
        if quantidade:
            updates.append(f"quantidade = '{quantidade}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE pedido SET {', '.join(updates)} WHERE endereco_filial = '{endereco_filial}' AND cnpj_fornec = '{cnpj_fornec}' AND idproduto = {id_produto}"
        return self.db.execute_statement(statement)

    def deleta_pedido(self, endereco_filial: str, cnpj_fornec: str, id_produto: int):
        statement = f"DELETE FROM pedido WHERE endereco_filial = '{endereco_filial}' AND cnpj_fornec = '{cnpj_fornec}' AND idproduto = {id_produto}"
        return self.db.execute_statement(statement)

