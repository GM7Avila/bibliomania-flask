FROM python:3.12
LABEL authors="GM7Avila"

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o diretório de trabalho no container
COPY . .

# Expor a porta da aplicação Flask
EXPOSE 5000

# Executar o script de inicialização e iniciar o servidor Flask
CMD ["sh", "-c", "python scripts/data_initializer_script.py && flask run --host=0.0.0.0"]
