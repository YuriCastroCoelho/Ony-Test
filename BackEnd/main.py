from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import models
from database import SessionLocal, engine

# Cria as tabelas no banco de dados, se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permite que o seu Front-end (React/Vercel) acesse esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo que define como o JSON vindo do Arduino deve ser recebido
class DadosArduino(BaseModel):
    tipo: str
    peso_porcentagem: int

# Variável em memória para acesso rápido pelo Dashboard
estado_atual_do_pote = {
    "racao": 0,
    "wifi": True
}

# Rota que o Dashboard (Front-end) usa para ler os dados
@app.get("/status")
def get_status():
    return estado_atual_do_pote

# --- ROTA ATUALIZADA PARA RECEBER JSON DO ARDUINO ---
@app.post("/atualizar")
def atualizar_pote(dados: DadosArduino):
    
    nivel_porcentagem = dados.peso_porcentagem
    
    
    estado_atual_do_pote["racao"] = nivel_porcentagem
    
    
    try:
        db = SessionLocal() 
        nova_leitura = models.LeituraPote(nivel_racao=nivel_porcentagem)
        db.add(nova_leitura)
        db.commit() 
        db.close()  
        print(f" -> Salvo no MySQL: {nivel_porcentagem}%")
    except Exception as erro_db:
        print(f" -> Erro ao salvar no banco: {erro_db}")
    
    return {"mensagem": "Dados recebidos com sucesso!", "valor": nivel_porcentagem}