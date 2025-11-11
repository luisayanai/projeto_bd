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
            conditions.append(f"iddevolucao = {id_devolucao}")
        if id_venda:
            conditions.append(f"idvenda = {id_venda}")
        if cpf_cliente:
            conditions.append(f"cpfcliente = '{cpf_cliente}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    
    def cadastra_devolucao(self, id_venda: int, credito: float, cpf_cliente: str):
        statement = f"INSERT INTO devolucao (idvenda, credito, cpfcliente) VALUES ({id_venda}, {credito}, '{cpf_cliente}')"
        
        return self.db.execute_statement(statement)

    def deleta_devolucao(self, id_devolucao: int):
        statement = f"DELETE FROM devolucao WHERE iddevolucao = {id_devolucao}"
        return self.db.execute_statement(statement)

