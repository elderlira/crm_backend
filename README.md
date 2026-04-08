# Run api

- source .venv/bin/activate
- install dependences

- uv sync
- run docker

- docker compose up -d

# acess postgres

- docker exec -it crm_postgres psql -U crm_user -d crm

# Create table in databse

- python manage.py makemigrations
- python manage.py migrate
- Update table in database

- python manage.py makemigrations authentication

# Create user

- python manage.py createuser

# Painel adm

- http://127.0.0.1:8000/admin

# Painel de rotas

- http://127.0.0.1:8000/api/