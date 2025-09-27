# Use a imagem oficial do Python como base
FROM python:3.9-slim-buster

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o diretório de trabalho
# ... (resto igual)
COPY . .
RUN python -c "from database import Base, engine; from models import *; Base.metadata.create_all(bind=engine)"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]