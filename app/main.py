import sys
import asyncio

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

