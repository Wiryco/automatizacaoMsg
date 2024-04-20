import dotenv
import os

dotenv.load_dotenv()

class querys():
    def __init__(self):
        self.dataBase = os.getenv('dataBase')
        self.schema = os.getenv('schema')

    def consultaDadosCliente(self):
        sql = f"""SELECT C.*, A.ID_TIPO_ENVIO, B.DESCRICAO_TIPO_ENVIO, A.ID_MENSAGEM, A.CAMINHO_ARQUIVO, D.DESCRICAO_MENSAGEM
                FROM {self.dataBase}.{self.schema}.CONTROLE_ENVIO_WPP A
                JOIN {self.dataBase}.{self.schema}.TIPO_ENVIO_WPP B ON A.ID_TIPO_ENVIO = B.ID_TIPO_ENVIO
                JOIN {self.dataBase}.{self.schema}.CONTATOS_WPP C ON A.ID_CONTATO = C.ID_CONTATO
                JOIN {self.dataBase}.{self.schema}.MENSAGEM_WPP D ON A.ID_MENSAGEM = D.ID_MENSAGEM
                WHERE C.ATIVO = 1"""

        return sql