# This project is developeding with python 3.7, Django and PostgreSQL.
How to install?
1) git clone https://github.com/Fox-sys/History.git
2) cd history
3) python3 -m venv venv
4) source venv/bin/activate 
5) pip3 install -r req.txt
6) cd  history
7) enter info for your database in history/settings.py
8) python3 manage.py makemigrations && python3 manage.py migrate
9) python3 manage.py runserver

# update comment:
First alpha version of this projects. There are still to many bugs to fix

# Patch Note:
1) Added page for changing password
2) Some small fixes for fill_db script