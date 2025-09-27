📌 Projeto Backend – FakeStore

Este projeto é um MVP fullstack containerizado:

Front-end: Aplicação React (build com Vite, servida por Nginx).
Back-end: API FastAPI (Python) com persistência em SQLite. Integração:
4 métodos HTTP (POST/GET/PUT/DELETE) para gerenciamento de pedidos,
+ produtos da Fake Store API externa. Tecnologias: Docker Compose para orquestração,
+  volumes para persistir o banco de dados.

Este repositório contém o backend do projeto FakeStore, responsável por fornecer a API REST para o frontend e gerenciar a lógica de negócio.

fluxograma
<img width="1536" height="1024" alt="Fluxograma-mvp" src="https://github.com/user-attachments/assets/c36ad859-7ed0-41dc-bb92-06a1ffea34bf" />


📌Extrutura esperada

projeto-mvp/

backend/# Database

FakeStore-Frontend/# React app + Dockerfile + nginx.conf + .dockerignore

FakeStore-Backend/ # FastAPI + requirements.txt + Dockerfile

docker-compose.yml # Orquestração

⚙️ Instalação e Execução para Teste Local

  1.Clone o repositório(ou baixe do link https://github.com/csccorgozinho/Back-end-FakeStore-Sprint-Back-end-A-MVP-PUC-RIO):

    git clone https://github.com/csccorgozinho/Back-end-FakeStore-Sprint-Back-end-A-MVP-PUC-RIO.git
    cd FakeStore-Backend

  1.Instale Dependências:
    
    cd FakeStore-Backend # Vá para pasta backend
    python -m venv venv  
    # Ative venv:
    # Windows: venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt  # Instala FastAPI, Uvicorn, SQLAlchemy, Pydantic (~1-2 min)
    
  2.Inicie o Servidor:
  
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

  3.Teste o Back-End:

    entre em http://localhost:8000/docs (Swagger) para tester as funcionalidas do back-end
    Instalação e Execução com Docker

⚙️Instalação e Execução com Docker

Pré-requisitos
Docker Desktop: Instale a versão mais recente para sua plataforma:
Windows/macOS: Baixe de docker.com/products/docker-desktop. Ative WSL 2 no Windows (durante instalação).
Linux (Ubuntu/Debian): Rode no terminal:

sudo apt update

sudo apt install docker.io docker-compose

sudo usermod -aG docker $USER # Adicione seu usuário ao grupo docker (reinicie sessão)

Verifique instalação: docker --version e docker-compose --version (deve mostrar v2+).

Recursos Recomendados: 4GB+ RAM, 2+ CPU cores (Docker Settings > Resources para ajustar).

Rede: Conexão à internet para baixar imagens Docker (Node, Python, Nginx — ~1GB na primeira vez).
Navegador: Chrome/Firefox para testar (F12 para debug).
Construa e Inicie os Containers:

Rode o comando principal:

docker-compose up --build

Para rodar em background:
docker-compose up -d --build

Portas Mapeadas (Ajustáveis no docker-compose.yml):
Front-end: http://localhost:3000 (React app).
Back-end: http://localhost:8000 (API FastAPI).
