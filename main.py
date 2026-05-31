from fastapi import FastAPI
from database import conectar_banco

app = FastAPI(title="SIGAgro API", description="API para Gerenciamento Agrícola e Micro-irrigação")

@app.get("/")
def home():
    return {"status": "API SIGAgro rodando com sucesso!"}

# O erro 404 acontece quando esta linha abaixo (o decorator) está faltando ou com erro de digitação!
@app.get("/banco-status")
def checar_banco():
    try:
        # 1. Abre a conexão com o banco
        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        # 2. Executa um comando SQL real
        cursor.execute("SHOW TABLES;")
        tabelas = cursor.fetchall()
        
        # 3. Fecha a porta do cofre (muito importante!)
        conexao.close()
        
        # 4. Devolve o resultado
        return {
            "mensagem": "Conexão perfeita! O garçom encontrou o cofre.", 
            "tabelas_encontradas": tabelas
        }
    except Exception as e:
        return {"erro": f"Ops, falha ao conectar: {str(e)}"}