# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class ClienteFidelizadoDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_clientes_fidelizados(self, id_cadastro: int = None, cpf_cliente: str = None):
        query = "SELECT * FROM cliente_fidelizado"
        conditions = []
        if id_cadastro:
            conditions.append(f"idcadastro = {id_cadastro}")
        if cpf_cliente:
            conditions.append(f"cpfcliente = '{cpf_cliente}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_cliente_fidelizado_by_id(self, id_cadastro: int):
        query = f"SELECT * FROM cliente_fidelizado WHERE idcadastro = {id_cadastro}"
        return self.db.execute_select_one(query)
    
    def cadastra_cliente_fidelizado(self, id_cadastro: int, cpf_cliente: str, ponto: int = None, email: str = None):
        if ponto is not None and email:
            statement = f"INSERT INTO cliente_fidelizado (idcadastro, ponto, email, cpfcliente) VALUES ({id_cadastro}, {ponto}, '{email}', '{cpf_cliente}')"
        elif ponto is not None:
            statement = f"INSERT INTO cliente_fidelizado (idcadastro, ponto, cpfcliente) VALUES ({id_cadastro}, {ponto}, '{cpf_cliente}')"
        elif email:
            statement = f"INSERT INTO cliente_fidelizado (idcadastro, email, cpfcliente) VALUES ({id_cadastro}, '{email}', '{cpf_cliente}')"
        else:
            statement = f"INSERT INTO cliente_fidelizado (idcadastro, cpfcliente) VALUES ({id_cadastro}, '{cpf_cliente}')"
        
        return self.db.execute_statement(statement)

    def atualiza_cliente_fidelizado(self, id_cadastro: int, pontos: int = None, email: str = None, cpf_cliente: str = None):
        updates = []
        if pontos is not None:
            updates.append(f"ponto = {pontos}")
        if email:
            updates.append(f"email = '{email}'")
        if cpf_cliente:
            updates.append(f"cpfcliente = '{cpf_cliente}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE cliente_fidelizado SET {', '.join(updates)} WHERE idcadastro = {id_cadastro}"
        return self.db.execute_statement(statement)

    def deleta_cliente_fidelizado(self, id_cadastro: int):
        statement = f"DELETE FROM cliente_fidelizado WHERE idcadastro = {id_cadastro}"
        return self.db.execute_statement(statement)

