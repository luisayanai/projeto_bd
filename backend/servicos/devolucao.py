# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class DevolucaoDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    def get_devolucoes(self, id_devolucao: int = None, id_venda: int = None, cpf_cliente: str = None):
        query = "SELECT * FROM devolucao"
        conditions = []
        if id_devolucao:
            conditions.append(f"iddevolucao = {id_devolucao}")
        if id_venda:
            conditions.append(f"idvenda = {id_venda}")
        if cpf_cliente:
            conditions.append(f"cpfcliente = '{cpf_cliente}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_devolucao_by_id(self, id_devolucao: int):
        query = f"SELECT * FROM devolucao WHERE iddevolucao = {id_devolucao}"
        return self.db.execute_select_one(query)
    
    def cadastra_devolucao(self, id_devolucao: int, id_venda: int, credito: float, cpf_cliente: str):
        statement = f"INSERT INTO devolucao (iddevolucao, idvenda, credito, cpfcliente) VALUES ({id_devolucao}, {id_venda}, {credito}, '{cpf_cliente}')"
        
        return self.db.execute_statement(statement)

    def atualiza_devolucao(self, id_devolucao: int, id_venda: int = None, credito: float = None, cpf_cliente: str = None):
        updates = []
        if id_venda is not None:
            updates.append(f"idvenda = {id_venda}")
        if credito is not None:
            updates.append(f"credito = {credito}")
        if cpf_cliente:
            updates.append(f"cpfcliente = '{cpf_cliente}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE devolucao SET {', '.join(updates)} WHERE iddevolucao = {id_devolucao}"
        return self.db.execute_statement(statement)

    def deleta_devolucao(self, id_devolucao: int):
        statement = f"DELETE FROM devolucao WHERE iddevolucao = {id_devolucao}"
        return self.db.execute_statement(statement)

