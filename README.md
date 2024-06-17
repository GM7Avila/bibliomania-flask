# 📖 Bibliomania Project 
- Library Web System developed with Flask

## Technologies Used
- Flask
- SQLAlchemy
- MySQL
- Docker

## Setting Up the Development Environment
To get started with the Bibliomania project, follow these steps to build and run the application using Docker:

### 1. Build the Project:
- Use the provided Dockerfile to build the project:
```bash
docker compose build
```

### 2. Compose the Environment:
- Start the environment with Docker Compose:

```bash
docker compose up -d
```

This will initialize a container for the MySQL database locally and launch the Flask application. The -d flag runs the containers in detached mode, allowing you to continue using the terminal for other tasks.

### Accessing the Application
Once the environment is up and running, you can access the Flask application by navigating to http://localhost in your web browser.
