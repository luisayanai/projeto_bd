# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class VendaDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_vendas(self, id_venda: int = None, cpf_funcionario: str = None, cpf_cliente: str = None):
        query = "SELECT * FROM venda"
        conditions = []
        if id_venda:
            conditions.append(f"idvenda = {id_venda}")
        if cpf_funcionario:
            conditions.append(f"cpffuncionario = '{cpf_funcionario}'")
        if cpf_cliente:
            conditions.append(f"cpfcliente = '{cpf_cliente}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)
    
    def cadastra_venda(self, id_venda: int, data_compra: str, status: str, valor_desconto: float, cpf_funcionario: str, cpf_cliente: str, comissao: float, forma_pag: str = None, parcelas: int = None):
        if forma_pag and parcelas is not None:
            statement = f"INSERT INTO venda (idvenda, datacompra, status, valordesconto, cpffuncionario, cpfcliente, comissao, forma_pag, parcelas) VALUES ({id_venda}, '{data_compra}', '{status}', {valor_desconto}, '{cpf_funcionario}', '{cpf_cliente}', {comissao}, '{forma_pag}', {parcelas})"
        elif forma_pag:
            statement = f"INSERT INTO venda (idvenda, datacompra, status, valordesconto, cpffuncionario, cpfcliente, comissao, forma_pag) VALUES ({id_venda}, '{data_compra}', '{status}', {valor_desconto}, '{cpf_funcionario}', '{cpf_cliente}', {comissao}, '{forma_pag}')"
        elif parcelas is not None:
            statement = f"INSERT INTO venda (idvenda, datacompra, status, valordesconto, cpffuncionario, cpfcliente, comissao, parcelas) VALUES ({id_venda}, '{data_compra}', '{status}', {valor_desconto}, '{cpf_funcionario}', '{cpf_cliente}', {comissao}, {parcelas})"
        else:
            statement = f"INSERT INTO venda (idvenda, datacompra, status, valordesconto, cpffuncionario, cpfcliente, comissao) VALUES ({id_venda}, '{data_compra}', '{status}', {valor_desconto}, '{cpf_funcionario}', '{cpf_cliente}', {comissao})"
        
        return self.db.execute_statement(statement)

    def atualiza_venda(self, id_venda: int, data_compra: str = None, status: str = None, valor_desconto: float = None, cpf_funcionario: str = None, cpf_cliente: str = None, comissao: float = None, forma_pag: str = None, parcelas: int = None):
        updates = []
        if data_compra:
            updates.append(f"datacompra = '{data_compra}'")
        if status:
            updates.append(f"status = '{status}'")
        if valor_desconto is not None:
            updates.append(f"valordesconto = {valor_desconto}")
        if cpf_funcionario:
            updates.append(f"cpffuncionario = '{cpf_funcionario}'")
        if cpf_cliente:
            updates.append(f"cpfcliente = '{cpf_cliente}'")
        if comissao is not None:
            updates.append(f"comissao = {comissao}")
        if forma_pag:
            updates.append(f"forma_pag = '{forma_pag}'")
        if parcelas is not None:
            updates.append(f"parcelas = {parcelas}")
        
        if not updates:
            return False
        
        statement = f"UPDATE venda SET {', '.join(updates)} WHERE idvenda = {id_venda}"
        return self.db.execute_statement(statement)

    def deleta_venda(self, id_venda: int):
        statement = f"DELETE FROM venda WHERE idvenda = {id_venda}"
        return self.db.execute_statement(statement)

