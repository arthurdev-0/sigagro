from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import conectar_banco

app = FastAPI(title="SIGAgro API", description="API para Gerenciamento Agrícola e Micro-irrigação")

# Configuração do CORS para permitir que o Vue converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Libera qualquer front-end para testarmos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "API SIGAgro rodando com sucesso!"}

@app.get("/banco-status")
def checar_banco():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SHOW TABLES;")
        tabelas = cursor.fetchall()
        conexao.close()
        
        return {
            "mensagem": "Conexão perfeita! O garçom encontrou o cofre.", 
            "tabelas_encontradas": tabelas
        }
    except Exception as e:
        return {"erro": f"Ops, falha ao conectar: {str(e)}"}