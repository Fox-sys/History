# This project is developeding with python 3.7, Django, Docker and PostgreSQL.
How to install?
1) git clone https://github.com/Fox-sys/History.git
2) cd History
3) chmod +x history/entrypoint.sh
4) sudo docker-compose up --build
5) sudo docker-compose exec web python manage.py migrate
6) sudo docker-compose exec web python manage.py fill_db

Superuser account: SU 135790asz

# Patch Note:
Layout fix

