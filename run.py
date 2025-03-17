# run.py
from uvicorn import Config, Server
from uvicorn.config import LOGGING_CONFIG  # Importa a configuração padrão de logging
from app.main import app  # Importa a aplicação FastAPI do main.py

# Configuração do servidor
log_config = LOGGING_CONFIG  # Usa a configuração padrão do Uvicorn
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

config_kwargs = {
    "app": app,
    "host": "192.168.0.9",
    "port": 8080,
    "log_level": "info",
    "reload": True,
    "log_config": log_config,
}

# Cria e roda o servidor
if __name__ == "__main__":
    config = Config(**config_kwargs)
    web_server = Server(config=config)
    web_server.run()