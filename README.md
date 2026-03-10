## Run api

- source .venv/bin/activate

### install dependences

- uv sync

### run docker

- docker compose up -d

### acess postgres

- docker exec -it crm_postgres psql -U crm_user -d crm

### migrate tables

- python manage.py migrate authentication

## Insert role and users

-    INSERT INTO authentication_role (name, description) VALUES
    ('user', 'Usuário padrão'),
    ('supervisor', 'Supervisor do sistema'),
    ('admin', 'Administrador do sistema');



- INSERT INTO authentication_user (
    username,
    email,
    password,
    is_active,
    is_superuser,
    is_staff,
    first_name,
    last_name,
    role_id,
    date_joined
)
VALUES (
    'User', 
    'user@email.com',
    'pbkdf2_sha256$1200000$SaQzA10TSUSvHcf79DXYSa$NEuJ+GQ92M8u4385dfIzkUQnHrWIAvdbx4qPzqwR3OA=',
    TRUE,    -- is_active
    FALSE,   -- is_superuser
    FALSE,   -- is_staff
    '',      -- first_name
    '',      -- last_name
    1,       -- role_id
    NOW()    -- date_joined
);





