# Bibliomania Project
- Sistema Web de apoio à biblioteca desenvolvido em Flask

## 🛠️ Tecnologias utilizadas
- Flask
- SQLAlchemy
- Docker
- Bootstrap

### Banco de Dados - SQL
- MySQL

### Requisitos (pacotes)
- Instale os pacotes listados em `requirements.txt`
- Tenha o Docker instalado

### Utilização do Docker no Banco de Dados
- O container do banco foi mapeado para a porta 3333 do localhost;
- Para criação do container do banco de dados MySQL:

## Inicialize os Containers:
1. Construir Imagens Docker
```bash
docker-compose build
```

2. Inicialize o Container
```bash
docker-compose up
```
