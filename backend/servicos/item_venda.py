# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class ItemVendaDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_itens_venda(self, id_venda: int = None, id_produto: int = None):
        query = "SELECT * FROM item_venda"
        conditions = []
        if id_venda:
            conditions.append(f"idvenda = {id_venda}")
        if id_produto:
            conditions.append(f"idproduto = {id_produto}")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_item_venda(self, id_venda: int, id_produto: int):
        query = f"SELECT * FROM item_venda WHERE idvenda = {id_venda} AND idproduto = {id_produto}"
        return self.db.execute_select_one(query)
    
    def cadastra_item_venda(self, id_venda: int, id_produto: int, quantidade: str):
        statement = f"INSERT INTO item_venda (idvenda, idproduto, quantidade) VALUES ({id_venda}, {id_produto}, '{quantidade}')"
        
        return self.db.execute_statement(statement)

    def atualiza_item_venda(self, id_venda: int, id_produto: int, quantidade: str = None):
        updates = []
        if quantidade:
            updates.append(f"quantidade = '{quantidade}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE item_venda SET {', '.join(updates)} WHERE idvenda = {id_venda} AND idproduto = {id_produto}"
        return self.db.execute_statement(statement)

    def deleta_item_venda(self, id_venda: int, id_produto: int):
        statement = f"DELETE FROM item_venda WHERE idvenda = {id_venda} AND idproduto = {id_produto}"
        return self.db.execute_statement(statement)

