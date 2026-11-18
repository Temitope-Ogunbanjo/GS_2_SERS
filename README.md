# Citizen Assist AI - Energia API ⚡🤖

API backend desenvolvida em **FastAPI** para fornecer orientações de eficiência energética e recomendações inteligentes de eletrodomésticos com base nos dados oficiais do **PBE Inmetro**. O sistema utiliza uma arquitetura modular baseada em intenções e processamento de arquivos locais, eliminando dependências de web scraping em tempo de execução.

---

## 🚀 Funcionalidades

* **Consulta Local Otimizada:** Leitura e filtragem de datasets do Inmetro via Pandas de forma rápida e segura.
* **Dispatcher por Intenção:** Roteamento inteligente de requisições de linguagem natural para análise específica de cada categoria de aparelho (geladeiras, micro-ondas, TVs, etc.).
* **Documentação Interativa:** Swagger UI integrado (`/docs`) para testes e homologação rápida.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI** (Framework web assíncrono)
* **Uvicorn** (Servidor ASGI)
* **Pandas** (Manipulação e análise de dados tabulares)
* **Pydantic** (Validação de dados e tipagem)
* **Render.com** (Plataforma de deploy em nuvem)

---

## 📂 Estrutura do Projeto

```text
.
├── app/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── funcoes.py
│   └── main.py
├── CSV/                 # Datasets oficiais do PBE Inmetro
├── requirements.txt     # Dependências do projeto
├── runtime.txt          # Versão do Python configurada para o ambiente
└── README.md
```

## 🧪 Como Executar Localmente

1. Clone o repositório:

   **Bash**

   ```bash
   git clone https://github.com/Temitope-Ogunbanjo/GS_2_SERS.git
   cd GS_2_SERS
   ```

2. Crie e ative um ambiente virtual:

   **Bash**

   ```bash
   python -m venv .venv

   # No Windows:
   .venv\Scripts\activate

   # No Linux/Mac:
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor localmente com Uvicorn:

   ```bash
   uvicorn app.main:App --reload
   ```

5. Acesse a documentação interativa em:

   `http://127.0.0.1:8000/docs`

## 👥 Equipe de Desenvolvimento

- **Gabriel Oliveira Gusmão Florêncio dos Santos** — RM 573747
- **Gustavo de Souza Abreu** — RM 574080
- **Temitope Kuku da Silva Ogunbanjo** — RM 573772

***[Clique aqui para acessar o vídeo explicativo e demonstrativo no youtube](https://youtu.be/I4uxKGNxGjc?si=hhS7Dvmrrg4sGbem)***
