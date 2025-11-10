# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class ClienteDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_clientes(self, cpf: str = None):
        query = "SELECT * FROM cliente"
        if cpf:
            query += f" WHERE cpf = '{cpf}'"
        
        return self.db.execute_select_all(query)

    ''' redundante com a get_clientes?????
    def get_cliente_by_cpf(self, cpf: str): 
        query = f"SELECT * FROM cliente WHERE cpf = '{cpf}'"
        return self.db.execute_select_one(query)
    '''

    def cadastra_cliente(self, cpf: str, nome: str, endereco: str = None):
        if endereco:
            statement = f"INSERT INTO cliente (cpf, nome, endereco) VALUES ('{cpf}', '{nome}', '{endereco}')"
        else:
            statement = f"INSERT INTO cliente (cpf, nome) VALUES ('{cpf}', '{nome}')"
        
        return self.db.execute_statement(statement)

    def atualiza_cliente(self, cpf: str, nome: str = None, endereco: str = None):
        updates = []
        if nome:
            updates.append(f"nome = '{nome}'")
        if endereco:
            updates.append(f"endereco = '{endereco}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE cliente SET {', '.join(updates)} WHERE cpf = '{cpf}'"
        return self.db.execute_statement(statement)

    def deleta_cliente(self, cpf: str):
        statement = f"DELETE FROM cliente WHERE cpf = '{cpf}'"
        return self.db.execute_statement(statement)

