FROM python:3.12
LABEL authors="GM7Avila"

#  diretório de trabalho dentro do container
WORKDIR /app

# requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do código para o diretório de trabalho no container
COPY . .

# Executa o script de inicialização e inicia o servidor Flask
CMD ["sh", "-c", "python scripts/data_initializer_script.py && flask run --host=0.0.0.0"]
