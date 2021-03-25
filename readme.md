# This project is developeding with python 3.7, Django, Docker and PostgreSQL.
How to install?
1) git clone https://github.com/Fox-sys/History.git
2) cd History
3) fill '.env.prod' and '.env.prod.db' with following templates: 
    ## .env.prod:
    - DEBUG=0
    - SECRET_KEY=your secret key
    - DJANGO_ALLOWED_HOSTS=your hosts [::1]
    - SQL_ENGINE=django.db.backends.postgresql
    - SQL_DATABASE=your database (get from .env.prod.db)
    - SQL_USER=your user (get from .env.prod.db)
    - SQL_PASSWORD=your password (get from .env.prod.db)
    - SQL_HOST=db
    - SQL_PORT=5432
    - DATABASE=postgres
    ## .env.prod.db:
    - POSTGRES_USER=your user
    - POSTGRES_PASSWORD=your password
    - POSTGRES_DB=your database
4) chmod +x app/entrypoint.prod.sh
5) sudo docker-compose -f docker-compose.prod.yml up --build
6) sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
7) sudo docker-compose -f docker-compose.prod.yml exec web python manage.py fill_db
8) sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic

Superuser account: SU 135790asz

# Patch Note:
Dev Version: 1.1.1

- changed password validation