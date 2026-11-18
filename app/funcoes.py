import os
import pandas as pd

PASTA_CSV = "csv"

def Televisores(Limite : 5):

    Path = os.path.join(PASTA_CSV, "Televisores.csv")
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação correta
    DF["Consumo_num"] = pd.to_numeric(DF["Consumo (kWh/mês)"], errors="coerce")
    DF["Standby_num"] = pd.to_numeric(DF["Potência Modo Espera (Stand-by) (W)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A (removendo espaços e maiúsculas/minúsculas)
    if "Classificação" in DF.columns:
        DF_Filtrado = DF[DF["Classificação"].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Caso não ache nenhum Classificação A, usa o dataframe inteiro como fallback
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Menor consumo mensal primeiro, depois menor stand-by
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Consumo_num", "Standby_num"], 
        ascending=[True, True]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite) 

    # 5. Monta a lista estruturada para o retorno da API
    Resultados = []
    for _, Row in Melhores.iterrows():
        Resultados.append({
            "modelo" : Row.get("Modelo", "N/D"),
            "marca" : Row.get("Marca", "N/D"),
            "status_modelo": Row.get("Status do Modelo", "N/D"),
            "tipo": Row.get("Tipo", "N/D"),
            "tensao": Row.get("Tensão (V)", "N/D"),
            "consumo_kwh_mes": Row.get("Consumo (kWh/mês)", "N/D"),
            "standby_w": Row.get("Potência Modo Espera (Stand-by) (W)", "N/D"),
            "tamanho_polegadas": Row.get("Diagonal em polegadas", "N/D"),
            "classificacao": Row.get("Classificação", "N/D"),
            "registro": Row.get("Número do Registro", "N/D")
        })

    return {
        "Categoria": "Televisores",
        "criterio_utilizado": "Apenas Classificação A, ordenados por menor consumo mensal e menor potência em stand-by.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(Resultados),
        "modelos_ideais": Resultados,
        "recomendacoes": [
            "Ative o modo de economia de energia (Eco Mode) nas configurações da tela.",
            "Desligue o aparelho da tomada quando ausente por longos períodos para zerar totalmente o consumo em stand-by.",
            "Ajuste a luz de fundo (Backlight) para um nível confortável e não máximo."
        ]
    }
def Microondas(Limite : 5):

    Path = os.path.join(PASTA_CSV, "Fornos_Microondas.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Consumo_Standby_num"] = pd.to_numeric(DF["Consumo Modo Espera (Stand-by) (kWh/dia)"], errors="coerce")
    DF["Eficiencia_num"] = pd.to_numeric(DF["Eficiência Energética (%)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A (coluna: Classificação Eficiência Energética)
    Classificacao = "Classificação Eficiência Energética"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Menor consumo em stand-by (kWh/dia) e maior eficiência (%)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Consumo_Standby_num", "Eficiencia_num"], 
        ascending=[True, False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tensao": row.get("Tensão (V)", "N/D"),
            "volume_util_l": row.get("Volume Útil (l)", "N/D"),
            "potencia_nominal_w": row.get("Potência Nominal (W)", "N/D"),
            "consumo_standby_kwh_dia": row.get("Consumo Modo Espera (Stand-by) (kWh/dia)", "N/D"),
            "eficiencia_energetica_pct": row.get("Eficiência Energética (%)", "N/D"),
            "classificacao": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Fornos Micro-ondas",
        "criterio_utilizado": "Apenas Classificação A, ordenados por menor consumo em stand-by e maior eficiência energética.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Desligue o micro-ondas da tomada quando não estiver em uso para zerar o consumo do relógio em modo stand-by.",
            "Descongele os alimentos com antecedência na geladeira para reduzir drasticamente o tempo de uso do aparelho.",
            "Utilize recipientes adequados que permitam o aquecimento uniforme, evitando reaquecimentos desnecessários."
        ]
    }
def MaquinaLavar(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Maquina_Lavar.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Consumo_Ciclo_Frio_num"] = pd.to_numeric(DF["Consumo de energia (kWh/ciclo) água fria"], errors="coerce")
    DF["Consumo_Agua_num"] = pd.to_numeric(DF["Consumo de água (l)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A (coluna: Faixa de Classificação Global)
    Classificacao = "Faixa de Classificação Global"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Menor consumo de energia por ciclo (água fria) e menor consumo de água (l)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Consumo_Ciclo_Frio_num", "Consumo_Agua_num"], 
        ascending=[True, True]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tipo_lavadora": row.get("Tipo de Lavadora", "N/D"),
            "tensao": row.get("Tensão (V)", "N/D"),
            "capacidade_kg": row.get("Capacidade de lavagem (kg)", "N/D"),
            "consumo_ciclo_frio_kwh": row.get("Consumo de energia (kWh/ciclo) água fria", "N/D"),
            "consumo_agua_litros": row.get("Consumo de água (l)", "N/D"),
            "velocidade_centrifugacao_rpm": row.get("Velocidade de centrifugação (rpm)", "N/D"),
            "tempo_ciclo_min": row.get("Tempo do ciclo (min)", "N/D"),
            "classificacao": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Máquinas de Lavar Roupas",
        "criterio_utilizado": "Apenas Classificação Global A, ordenados por menor consumo de energia por ciclo (água fria) e menor consumo de água.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Utilize a capacidade máxima de carga indicada pelo fabricante em cada lavagem para evitar o desperdício de água e energia com ciclos parciais.",
            "Dose o sabão e o amaciante corretamente conforme a recomendação; o excesso de espuma força o motor e exige mais enxágues.",
            "Sempre que possível, realize as lavagens utilizando água fria, eliminando o gasto energético com resistências de aquecimento."
        ]
    }
def Refrigeradores(Limite : int =5):
    Path = os.path.join(PASTA_CSV, "Refrigeradores.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Consumo_Mensal_num"] = pd.to_numeric(DF["Consumo Médio de Energia Mensal (kWh/mês)"], errors="coerce")
    DF["Volume_Total_num"] = pd.to_numeric(DF["Volume Total (litros)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A (priorizando a classe de eficiência 2025 ou padrão)
    Classificacao = "Classe de Eficiência Energética Padrão 2025"
    if Classificacao not in DF.columns:
        Classificacao = "Classe de Eficiência Energética Padrão 2022"

    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Menor consumo médio mensal (kWh/mês) e maior volume total (l)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Consumo_Mensal_num", "Volume_Total_num"], 
        ascending=[True, False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tipo": row.get("Tipo", "N/D"),
            "tensao": row.get("Tensão (V)", "N/D"),
            "sistema_degelo": row.get("Sistema de Degelo", "N/D"),
            "volume_total_litros": row.get("Volume Total (litros)", "N/D"),
            "consumo_mensal_kwh": row.get("Consumo Médio de Energia Mensal (kWh/mês)", "N/D"),
            "classificacao_energetica": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Refrigeradores e Assemelhados",
        "criterio_utilizado": f"Apenas Classe de Eficiência A ({Classificacao}), ordenados por menor consumo médio mensal e maior volume total.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Verifique regularmente se as borrachas de vedação da porta estão vedando perfeitamente para evitar a fuga de ar frio.",
            "Evite encostar o refrigerador diretamente em fontes de calor, como o fogão ou áreas com incidência direta de luz solar.",
            "Não guarde alimentos ainda quentes no interior do refrigerador e evite manter a porta aberta por longos períodos."
        ]
    }
def Aquecimento_Solar_Agua(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Aquecimento_Solar_Agua.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    # Nota: No CSV de aquecimento solar, a coluna de produção por coletor pode vir formatada com texto ou números
    col_producao = "Por Coletor (KWh/mês)" if "Por Coletor (KWh/mês)" in DF.columns else DF.columns[2]
    col_eficiencia = "Eficiência Média Energética (%)" if "Eficiência Média Energética (%)" in DF.columns else DF.columns[4]

    DF["Producao_num"] = pd.to_numeric(DF[col_producao], errors="coerce")
    DF["Eficiencia_num"] = pd.to_numeric(DF[col_eficiencia], errors="coerce")

    # 2. Filtra estritamente por Classificação A (coluna: Classificação)
    Classificacao = "Classificação"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior eficiência energética (%) e maior produção média mensal (KWh/mês)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Eficiencia_num", "Producao_num"], 
        ascending=[False, False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "volume_sistema_litros": row.get("Volume do Sistema (litros)", "N/D"),
            "area_externa_coletor_m2": row.get("Area Externa do Coletor (M²)", "N/D"),
            "producao_por_coletor_kwh_mes": row.get(col_producao, "N/D"),
            "eficiencia_energetica_pct": row.get(col_eficiencia, "N/D"),
            "material_superficie": row.get("Material Superfície Absorvedora", "N/D"),
            "classificacao": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Sistemas acoplados - Equipamentos de aquecimento solar de água",
        "criterio_utilizado": "Apenas Classificação A, ordenados por maior eficiência média energética e maior produção mensal de energia.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Realize manutenções e limpezas periódicas nos coletores solares para evitar o acúmulo de poeira e manter a máxima absorção térmica.",
            "Dimensionar corretamente o volume do reservatório térmico (boiler) de acordo com o consumo diário da residência para evitar uso excessivo da resistência elétrica de apoio.",
            "Certifique-se de que a orientação e inclinação dos coletores estejam otimizadas para a latitude local, garantindo maior captação de insolação ao longo do ano."
        ]
    }
def Ventilador_Teto(Limite : int = 5):

    Path = os.path.join(PASTA_CSV, "Ventilador_Teto.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Eficiencia_Alta_num"] = pd.to_numeric(DF["Eficiência na velocidade alta [(m³/s)/W]"], errors="coerce")
    DF["Consumo_Alta_num"] = pd.to_numeric(DF["Consumo de energia mensal na vel. alta (kWh/mês)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A na velocidade alta
    Classificacao = "Faixa de classificação na velocidade alta"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior eficiência na velocidade alta e menor consumo mensal na vel. alta
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Eficiencia_Alta_num", "Consumo_Alta_num"], 
        ascending=[False, True]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tensao": row.get("Tensão (V)", "N/D"),
            "diametro_cm": row.get("Diâmetro (cm)", "N/D"),
            "numero_de_pas": row.get("Número de pás", "N/D"),
            "material_da_pa": row.get("Material da pá", "N/D"),
            "eficiencia_velocidade_alta": row.get("Eficiência na velocidade alta [(m³/s)/W]", "N/D"),
            "consumo_mensal_alta_kwh": row.get("Consumo de energia mensal na vel. alta (kWh/mês)", "N/D"),
            "classificacao_alta": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Ventilador de Teto de Uso Residencial",
        "criterio_utilizado": "Apenas Classificação A na velocidade alta, ordenados por maior eficiência energética [(m³/s)/W] e menor consumo mensal.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Desligue o ventilador de teto ao sair do ambiente para evitar o desperdício desnecessário de energia em cômodos vazios.",
            "Utilize as velocidades média ou baixa durante a noite ou em dias amenos, pois reduzem significativamente o consumo elétrico.",
            "Realize a limpeza periódica das pás para evitar o acúmulo de poeira, o que afeta a aerodinâmica e diminui a eficiência da ventilação."
        ]
    }
def Ventiladores_Mesa(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Ventilador_Mesa.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Eficiencia_Alta_num"] = pd.to_numeric(DF["Eficiência (m3/s/W) (Alta)"], errors="coerce")
    DF["Consumo_Alta_num"] = pd.to_numeric(DF["Consumo de Energia Mensal(kWh/mês) (Alta)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A na velocidade alta
    Classificacao = "Classificação (Alta)"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior eficiência na velocidade alta e menor consumo mensal na vel. alta
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Eficiencia_Alta_num", "Consumo_Alta_num"], 
        ascending=[False, True]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tipo_produto": row.get("Tipo de Produto", "N/D"),
            "tensao": row.get("Tensão", "N/D"),
            "diametro_helice_cm": row.get("Diâmetro da Hélice (cm)", "N/D"),
            "numero_de_pas": row.get("No. de Pás", "N/D"),
            "eficiencia_velocidade_alta": row.get("Eficiência (m3/s/W) (Alta)", "N/D"),
            "consumo_mensal_alta_kwh": row.get("Consumo de Energia Mensal(kWh/mês) (Alta)", "N/D"),
            "classificacao_alta": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Ventiladores de mesa, de coluna e circulador de ar",
        "criterio_utilizado": "Apenas Classificação A na velocidade alta, ordenados por maior eficiência energética (m³/s/W) e menor consumo mensal.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Desligue o ventilador de mesa ou coluna sempre que o ambiente estiver desocupado.",
            "Posicione o aparelho em locais estratégicos para favorecer a circulação cruzada do ar, permitindo o uso de velocidades menores.",
            "Limpe a grade e a hélice periodicamente para evitar o acúmulo de poeira que reduz o fluxo de ar e força o motor."
        ]
    }
def Aquecimento_Gas_Agua(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Aquecimento_Gas_Agua.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    # Nota: Usamos o rendimento percentual (%) para avaliar a eficiência de conversão energética
    col_rendimento = "Rendimento (%)" if "Rendimento (%)" in DF.columns else DF.columns[7]
    DF["Rendimento_num"] = pd.to_numeric(DF[col_rendimento], errors="coerce")

    # 2. Filtra estritamente por Classificação A (coluna: Classificação  PBE)
    Classificacao = "Classificação  PBE" if "Classificação  PBE" in DF.columns else "Classificação"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior rendimento energético (%)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Rendimento_num"], 
        ascending=[False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", row.get("Status do Modelo", "N/D")), # Ajuste conforme a primeira coluna do exemplo
            "modelo": row.get("Modelo", row.get("316FTBE", "N/D")),
            "capacidade_vazao_l_min": row.get("Capacidade de Vazão (litros/min)", "N/D"),
            "tipo_gas": row.get("Tipo de Gás", "N/D"),
            "rendimento_pct": row.get(col_rendimento, "N/D"),
            "selo_conpet": row.get("Selo CONPET", "N/D"),
            "classificacao": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Aquecedores de água a gás, dos tipos instantâneo e de acumulação",
        "criterio_utilizado": "Apenas Classificação A no PBE, ordenados por maior rendimento energético (%).",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Realize a manutenção preventiva e a desincrustação do trocador de calor anualmente para garantir a máxima eficiência na queima de gás.",
            "Ajuste a temperatura de saída da água no aquecedor para um nível confortável (evitando misturar muita água fria nos registros), reduzindo o consumo de gás.",
            "Certifique-se de que a instalação da chaminé atenda estritamente às normas técnicas de exaustão para garantir segurança e eficiência operacional."
        ]
    }
def Lampada_Vapor(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Lampada_Vapor.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Eficiencia_num"] = pd.to_numeric(DF["Eficiência Luminosa(lm/W)"], errors="coerce")
    DF["Fluxo_num"] = pd.to_numeric(DF["Fluxo Luminoso (lm)"], errors="coerce")

    # 2. Ordenação inteligente: Maior eficiência luminosa (lm/W) e maior fluxo luminoso (lm)
    DF_Ordenado = DF.sort_values(
        by=["Eficiencia_num", "Fluxo_num"], 
        ascending=[False, False]
    )

    # 3. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 4. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tensao": row.get("Tensão (V)", "N/D"),
            "potencia_w": row.get("Potência (W)", "N/D"),
            "fluxo_luminoso_lm": row.get("Fluxo Luminoso (lm)", "N/D"),
            "eficiencia_luminosa_lm_w": row.get("Eficiência Luminosa(lm/W)", "N/D"),
            "vida_mediana_horas": row.get("Vida Mediana(horas)", "N/D"),
            "selo_procel": row.get("Selo Procel", "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Lâmpada de vapor de sódio à alta pressão",
        "criterio_utilizado": "Ordenados por maior eficiência luminosa (lm/W) e maior fluxo luminoso.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Utilize reatores de alta eficiência compatíveis para evitar perdas energéticas no sistema de acendimento.",
            "Planeje a iluminação externa ou industrial considerando o tempo de aquecimento característico dessas lâmpadas."
        ]
    }
def Lampada_Fluorescente(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Lampada_Florescente.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Eficiencia_num"] = pd.to_numeric(DF["Eficiência Luminosa (lm/W)"], errors="coerce")

    # 2. Filtra estritamente por Classificação A
    Classificacao = "Classificação Eficiência Energética"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior eficiência luminosa (lm/W)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Eficiencia_num"], 
        ascending=[False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "potencia_w": row.get("Potência (W)", "N/D"),
            "fluxo_luminoso_lm": row.get("Fluxo Luminoso (lm)", "N/D"),
            "eficiencia_luminosa_lm_w": row.get("Eficiência Luminosa (lm/W)", "N/D"),
            "equivalencia_incandescente": row.get("Equivalência lâmpada Incandescente", "N/D"),
            "classificacao": row.get(Classificacao, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Lâmpadas fluorescentes compactas com reator integrado à base",
        "criterio_utilizado": "Apenas Classificação A, ordenados por maior eficiência luminosa (lm/W).",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Evite o acionamento excessivo e de curta duração, pois ciclos frequentes reduzem a vida útil da lâmpada fluorescente.",
            "Em caso de quebra, manuseie com cuidado devido à presença de vapor de mercúrio e faça o descarte em pontos de coleta especializados."
        ]
    }
def Lampada_Led(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Lampada_Led.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    DF["Eficiencia_num"] = pd.to_numeric(DF["Eficiência Luminosa (lm/W)"], errors="coerce")
    DF["Vida_num"] = pd.to_numeric(DF["Vida Útil Nominal (horas)"], errors="coerce")

    # 2. Ordenação inteligente: Maior eficiência luminosa (lm/W) e maior vida útil nominal (horas)
    DF_Ordenado = DF.sort_values(
        by=["Eficiencia_num", "Vida_num"], 
        ascending=[False, False]
    )

    # 3. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 4. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tipo_lampada": row.get("Tipo de Lâmpada", "N/D"),
            "potencia_w": row.get("Potência (W)", "N/D"),
            "fluxo_luminoso_lm": row.get("Fluxo Luminoso (lm)", "N/D"),
            "eficiencia_luminosa_lm_w": row.get("Eficiência Luminosa (lm/W)", "N/D"),
            "vida_util_horas": row.get("Vida Útil Nominal (horas)", "N/D"),
            "selo_procel": row.get("Selo Procel", "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Lâmpadas LED com Dispositivo Integrado à Base",
        "criterio_utilizado": "Ordenados por maior eficiência luminosa (lm/W) e maior vida útil nominal.",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Prefira lâmpadas LED com Selo Procel A para garantir o máximo aproveitamento energético.",
            "Desligue as luzes ao se ausentar de ambientes por períodos prolongados, aproveitando a durabilidade superior do LED frente a ciclos de liga/desliga."
        ]
    }
def Fornos(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Fogoes_Fornos.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    col_rendimento = "Rendimento Médio dos Queimadores (%)" if "Rendimento Médio dos Queimadores (%)" in DF.columns else DF.columns[6]
    DF["Rendimento_num"] = pd.to_numeric(DF[col_rendimento], errors="coerce")

    # 2. Filtra estritamente por Classificação PBE Mesa de Coccão ou Forno
    Classificacao = "Classificação PBE Mesa de Coccão" if "Classificação PBE Mesa de Coccão" in DF.columns else "Classificação PBE Forno"
    if Classificacao in DF.columns:
        DF_Filtrado = DF[DF[Classificacao].astype(str).str.strip().str.upper() == "A"].copy()
    else:
        DF_Filtrado = DF.copy()

    # Fallback se não encontrar Classificação A exata
    if DF_Filtrado.empty:
        DF_Filtrado = DF.copy()

    # 3. Ordenação inteligente: Maior rendimento médio dos queimadores (%)
    DF_Ordenado = DF_Filtrado.sort_values(
        by=["Rendimento_num"], 
        ascending=[False]
    )

    # 4. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 5. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tipo_produto": row.get("Tipo de Produto", "N/D"),
            "tipo_gas": row.get("Tipo de Gás", "N/D"),
            "rendimento_medio_pct": row.get(col_rendimento, "N/D"),
            "volume_forno_litros": row.get("Volume do Forno (litros)", "N/D"),
            "classificacao_mesa": row.get("Classificação PBE Mesa de Coccão", "N/D"),
            "classificacao_forno": row.get("Classificação PBE Forno", "N/D"),
            "selo_conpet": row.get("Selo CONPET", "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Fogões e Fornos a Gás de Uso Doméstico",
        "criterio_utilizado": "Apenas Classificação A, ordenados por maior rendimento médio dos queimadores (%).",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Utilize panelas com fundo plano e diâmetro compatível com o queimador para evitar a dispersão lateral da chama.",
            "Mantenha os queimadores limpos e desentupidos para assegurar uma queima eficiente e homogênea do gás.",
            "Evite abrir a porta do forno desnecessariamente durante o cozimento para prevenir perdas térmicas e gasto excessivo de gás."
        ]
    }
def Fornos_Eletricos(Limite: int = 5):

    Path = os.path.join(PASTA_CSV, "Fornos_Eletricos.csv") 
    if not os.path.exists(Path):
        return {"erro": f"Arquivo de {Path} não encontrado"}

    DF = pd.read_csv(Path)

    # 1. Normaliza as colunas numéricas para ordenação
    col_consumo = "Consumo de Energia Elétrica (kWh)" if "Consumo de Energia Elétrica (kWh)" in DF.columns else DF.columns[7]
    DF["Consumo_num"] = pd.to_numeric(DF[col_consumo], errors="coerce")

    # 2. Ordenação inteligente: Menor consumo de energia elétrica (kWh)
    DF_Ordenado = DF.sort_values(
        by=["Consumo_num"], 
        ascending=[True]
    )

    # 3. Pega a quantidade exata definida pela variável 'limite'
    Melhores = DF_Ordenado.head(Limite)

    # 4. Monta a lista estruturada para o retorno da API
    lista_resultados = []
    for _, row in Melhores.iterrows():
        lista_resultados.append({
            "marca": row.get("Marca", "N/D"),
            "modelo": row.get("Modelo", "N/D"),
            "tensao_nominal_v": row.get("Tensão Nominal (V)", "N/D"),
            "volume_util_l": row.get("Volume Útil (l)", "N/D"),
            "potencia_nominal_kw": row.get("Potência Nominal (kW)", "N/D"),
            "consumo_energia_kwh": row.get(col_consumo, "N/D"),
            "registro": row.get("Número do Registro", "N/D")
        })

    return {
        "categoria": "Fornos Elétricos Comerciais",
        "criterio_utilizado": "Ordenados por menor consumo de energia elétrica (kWh).",
        "quantidade_solicitada": Limite,
        "total_encontrados": len(lista_resultados),
        "modelos_ideais": lista_resultados,
        "recomendacoes": [
            "Programe o pré-aquecimento do forno elétrico apenas pelo tempo estritamente necessário para a receita.",
            "Aproveite o calor residual desligando o forno alguns minutos antes de finalizar o preparo dos alimentos.",
            "Realize a limpeza interna periódica para preservar a refletividade das paredes e garantir a eficiência térmica."
        ]
    }