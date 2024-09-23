.PHONY: up down makemigrations migrate tests

DOCKER_COMPOSE_FILE = docker-compose.yml

# Target para rodar o Docker Compose
up: down
	@if [ "$$FORCE" = "true" ]; then docker system prune --all -f; fi
	@rm -rf data/
	docker-compose up --build

down:
	docker-compose down --volumes
	@if [ "$$FORCE" = "true" ]; then docker system prune --all -f; fi
	@rm -rf data/

# Target para gerar migrations
makemigrations:
	docker exec web python manage.py makemigrations

# Target para aplicar migrations
migrate:
	docker exec web python manage.py makemigrations
	docker exec web python manage.py migrate

# Target para rodar testes
tests:
	docker exec web python manage.py test core.tests -v 2

# Lista de comandos
help:
	@echo "Comandos disponíveis:"
	@echo "  make up -f           - Sobe os containers Docker, faz build e limpa o sistema com a flag -f (opcional)"
	@echo "  make down -f         - Derruba os containers Docker, limpa volumes e opcionalmente com -f, limpa o sistema"
	@echo "  make makemigrations  - Cria novas migrações com o Django"
	@echo "  make migrate         - Aplica migrações do Django"
	@echo "  make tests           - Roda testes unitários com o Django"