import re
from app.funcoes import (
    Microondas,
    Televisores,
    MaquinaLavar,
    Refrigeradores,
    Aquecimento_Solar_Agua,
    Ventilador_Teto,
    Ventiladores_Mesa,
    Aquecimento_Gas_Agua,
    Lampada_Vapor,
    Lampada_Fluorescente,
    Lampada_Led,
    Fornos,
    Fornos_Eletricos
)

def ProcessarMensagem(mensagem: str):
    """
    Analisa uma mensagem vaga/natural do usuário, identifica a categoria e a intenção,
    e retorna os dados estruturados (modelos ideais ou recomendações de economia).
    """
    msg_lower = mensagem.lower()
    
    # 1. Identificar a Categoria com base em palavras-chave na frase
    categoria_alvo = None
    if any(k in msg_lower for k in ["micro-ondas", "microondas"]):
        categoria_alvo = "microondas"
    elif any(k in msg_lower for k in ["tv", "televisor", "televisão"]):
        categoria_alvo = "televisor"
    elif any(k in msg_lower for k in ["maquina de lavar", "lavadora", "lavar roupas"]):
        categoria_alvo = "lavadora"
    elif any(k in msg_lower for k in ["geladeira", "refrigerador", "freezer"]):
        categoria_alvo = "refrigerador"
    elif any(k in msg_lower for k in ["aquecedor solar", "solar"]):
        categoria_alvo = "solar"
    elif any(k in msg_lower for k in ["ventilador de teto", "teto"]):
        categoria_alvo = "ventilador_teto"
    elif any(k in msg_lower for k in ["ventilador de mesa", "ventilador de coluna", "circulador"]):
        categoria_alvo = "ventilador_mesa"
    elif any(k in msg_lower for k in ["aquecedor a gás", "gas", "água a gás"]):
        categoria_alvo = "gas"
    elif any(k in msg_lower for k in ["lâmpada led", "led"]):
        categoria_alvo = "lampada_led"
    elif any(k in msg_lower for k in ["lâmpada fluorescente", "fluorescente"]):
        categoria_alvo = "lampada_fluorescente"
    elif any(k in msg_lower for k in ["lâmpada de vapor", "vapor de sódio"]):
        categoria_alvo = "lampada_vapor"
    elif any(k in msg_lower for k in ["fogão", "fogao", "cooktop"]):
        categoria_alvo = "fogao"
    elif any(k in msg_lower for k in ["forno elétrico", "forno eletrico"]):
        categoria_alvo = "forno_eletrico"

    if not categoria_alvo:
        return {
            "resposta": "Desculpe, não consegui identificar o eletrodoméstico ou categoria na sua pergunta. Poderia especificar melhor (ex: microondas, geladeira, televisor)?"
        }

    # 2. Identificar a Intenção (Se quer Dicas/Economia ou se quer Comprar/Modelos)
    quer_dicas = any(k in msg_lower for k in ["como economizar", "economizar", "gastar menos", "evitar desperdício", "dicas"])
    quer_comprar = any(k in msg_lower for k in ["qual", "comprar", "melhor", "indica", "sugestão", "recomendação", "quais"])

    # Por padrão, se não especificar claramente, entregamos os melhores modelos junto com as recomendações
    limite_padrao = 3

    # 3. Executar a função correspondente do seu analisador
    dados_resultado = {}
    if categoria_alvo == "microondas":
        dados_resultado = Microondas(Limite=limite_padrao)
    elif categoria_alvo == "televisor":
        dados_resultado = Televisores(Limite=limite_padrao)
    elif categoria_alvo == "lavadora":
        dados_resultado = MaquinaLavar(Limite=limite_padrao)
    elif categoria_alvo == "refrigerador":
        dados_resultado = Refrigeradores(Limite=limite_padrao)
    elif categoria_alvo == "solar":
        dados_resultado = Aquecimento_Solar_Agua(Limite=limite_padrao)
    elif categoria_alvo == "ventilador_teto":
        dados_resultado = Ventilador_Teto(Limite=limite_padrao)
    elif categoria_alvo == "ventilador_mesa":
        dados_resultado = Ventiladores_Mesa(Limite=limite_padrao)
    elif categoria_alvo == "gas":
        dados_resultado = Aquecimento_Gas_Agua(Limite=limite_padrao)
    elif categoria_alvo == "lampada_led":
        dados_resultado = Lampada_Led(Limite=limite_padrao)
    elif categoria_alvo == "lampada_fluorescente":
        dados_resultado = Lampada_Fluorescente(Limite=limite_padrao)
    elif categoria_alvo == "lampada_vapor":
        dados_resultado = Lampada_Vapor(Limite=limite_padrao)
    elif categoria_alvo == "fogao":
        dados_resultado = Fornos(Limite=limite_padrao)
    elif categoria_alvo == "forno_eletrico":
        dados_resultado = Fornos_Eletricos(Limite=limite_padrao)

    # 4. Formatar a resposta final para o chat baseada na intenção
    if quer_dicas and not quer_comprar:
        return {
            "intencao": "dicas_economia",
            "categoria": dados_resultado.get("categoria"),
            "recomendacoes": dados_resultado.get("recomendacoes", [])
        }
    
    # Resposta completa padrão (Modelos + Recomendações)
    return {
        "intencao": "recomendacao_completa",
        "mensagem_analisada": mensagem,
        "resultado": dados_resultado
    }