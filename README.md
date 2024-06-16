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


```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3333:3306 -d mysql
```

```
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
greenlet==3.0.3
importlib_metadata==7.1.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
mysql-connector-python==8.4.0
mysqlclient==2.2.4
SQLAlchemy==2.0.30
typing_extensions==4.11.0
Werkzeug==3.0.3
zipp==3.18.1
Flask-login==0.6.3
```



