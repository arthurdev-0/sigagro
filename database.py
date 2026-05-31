import pymysql

def conectar_banco():
    """
    Função responsável por abrir a porta do cofre (MySQL no Docker).
    """
    return pymysql.connect(
        host="127.0.0.1",
        user="admin_sigagro",
        password="secretpassword",
        database="sigagro",
        # O DictCursor faz com que os resultados do banco venham formatados
        # como Dicionários, o que facilita muito na hora de virar JSON!
        cursorclass=pymysql.cursors.DictCursor
    )