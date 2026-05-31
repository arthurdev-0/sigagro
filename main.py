from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import conectar_banco
from datetime import date

app = FastAPI(title="SIGAgro API", description="API para Gerenciamento Agrícola e Micro-irrigação")

# Configuração do CORS para permitir a comunicação com o Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de Dados: Define o formato exato que o Front-end deve enviar
class EquipamentoCreate(BaseModel):
    nome: str
    categoria: str  # Deve ser: 'Veiculo', 'Implemento', 'Irrigacao' ou 'Sensor'
    modelo: Optional[str] = None
    nro_serie_chassi: Optional[str] = None

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

# --------------------------------------------------------------------
# ROTA 1: Listar Equipamentos (Busca do MySQL e entrega pro Vue)
# --------------------------------------------------------------------
@app.get("/equipamentos")
def listar_equipamentos():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM equipamentos ORDER BY id DESC;")
        equipamentos = cursor.fetchall()
        conexao.close()
        return equipamentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar no banco: {str(e)}")

# --------------------------------------------------------------------
# ROTA 2: Cadastrar Equipamento (Recebe do Vue e salva no MySQL)
# --------------------------------------------------------------------
@app.post("/equipamentos")
def cadastrar_equipamento(equipamento: EquipamentoCreate):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        sql = """
            INSERT INTO equipamentos (nome, categoria, modelo, nro_serie_chassi, status, data_aquisicao)
            VALUES (%s, %s, %s, %s, 'Disponivel', %s);
        """
        data_hoje = date.today().strftime("%Y-%m-%d")
        
        cursor.execute(sql, (
            equipamento.nome,
            equipamento.categoria,
            equipamento.modelo,
            equipamento.nro_serie_chassi,
            data_hoje
        ))
        
        conexao.commit()
        conexao.close()
        return {"status": "sucesso", "mensagem": "Ativo registrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")