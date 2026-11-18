import sys
import asyncio
import os

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.chatbot import ProcessarMensagem

App = FastAPI(
    title="Citizen Assist AI - Energia API",
    description="API de análise de eficiência energética local baseada nos dados do PBE Inmetro.",
    version="2.0.0"
)

class MensagemChat(BaseModel):
    mensagem: str


@App.get("/")
def root():
    return {
        "status": "online",
        "servico": "Citizen Assist AI - Energia API (Modo Local CSV)",
        "documentacao": "/docs"
    }


@App.post("/api/chat/perguntar")
def perguntar_assistente(payload: MensagemChat):
    """
    Endpoint principal para o chatbot. Recebe mensagens em linguagem natural 
    (ex: 'Como economizar energia no microondas?' ou 'Qual televisor comprar?'),
    interpreta a intenção e retorna os dados dos CSVs locais do Inmetro.
    """
    if not payload.mensagem.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")
    
    resposta_processada = ProcessarMensagem(payload.mensagem)
    return resposta_processada


@App.get("/api/debug/arquivos")
def debug_arquivos():
    """
    Rota temporária para inspecionar a estrutura de diretórios no Render.
    """
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Tenta listar o diretório atual e o diretório pai
    conteudo_atual = os.listdir(diretorio_atual)
    
    raiz_projeto = os.path.dirname(diretorio_atual)
    conteudo_raiz = os.listdir(raiz_projeto) if os.path.exists(raiz_projeto) else "Raiz não existe"
    
    # Procura especificamente pela pasta csv ou data
    caminho_csv_possivel_1 = os.path.join(raiz_projeto, "csv")
    caminho_csv_possivel_2 = os.path.join(diretorio_atual, "csv")
    
    return {
        "diretorio_atual_script": diretorio_atual,
        "conteudo_diretorio_atual": conteudo_atual,
        "raiz_projeto": raiz_projeto,
        "conteudo_raiz": conteudo_raiz,
        "existe_csv_na_raiz": os.path.exists(caminho_csv_possivel_1),
        "conteudo_pasta_csv_raiz": os.listdir(caminho_csv_possivel_1) if os.path.exists(caminho_csv_possivel_1) else "Não encontrada",
        "existe_csv_no_atual": os.path.exists(caminho_csv_possivel_2),
    }