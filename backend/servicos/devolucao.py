# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class DevolucaoDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_devolucoes(self, id_devolucao: int = None, id_venda: int = None, cpf_cliente: str = None):
        query = "SELECT * FROM devolucao"
        conditions = []
        if id_devolucao:
            conditions.append(f"id_devolucao = {id_devolucao}")
        if id_venda:
            conditions.append(f"id_venda = {id_venda}")
        if cpf_cliente:
            conditions.append(f"cpf_cliente = '{cpf_cliente}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    
    def cadastra_devolucao(self, id_venda: int, id_produto: int, credito: float, cpf_cliente: str):
        statement = f"INSERT INTO devolucao (id_venda, id_produto, credito, cpf_cliente) VALUES ({id_venda}, {id_produto}, {credito}, '{cpf_cliente}')"
        
        return self.db.execute_statement(statement)

    def deleta_devolucao(self, id_devolucao: int):
        statement = f"DELETE FROM devolucao WHERE id_devolucao = {id_devolucao}"
        return self.db.execute_statement(statement)

