# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class FilialDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_filiais(self, endereco: str = None):
        query = "SELECT * FROM filial"
        if endereco:
            query += f" WHERE endereco = '{endereco}'"
        
        return self.db.execute_select_all(query)

    def get_filial_by_endereco(self, endereco: str):
        query = f"SELECT * FROM filial WHERE endereco = '{endereco}'"
        return self.db.execute_select_one(query)
    
    def cadastra_filial(self, endereco: str, cpf_gerente: str, telefone: int = None):
        # CPFGERENTE é NOT NULL no schema
        if telefone:
            statement = f"INSERT INTO filial (endereco, telefone, cpfgerente) VALUES ('{endereco}', {telefone}, '{cpf_gerente}')"
        else:
            statement = f"INSERT INTO filial (endereco, cpfgerente) VALUES ('{endereco}', '{cpf_gerente}')"
        
        return self.db.execute_statement(statement)

    def deleta_filial(self, endereco: str):
        statement = f"DELETE FROM filial WHERE endereco = '{endereco}'"
        return self.db.execute_statement(statement)

