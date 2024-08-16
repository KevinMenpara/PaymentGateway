python -m venv my_env

.\my_env\Scripts\activate

django-admin startproject src .

python manage.py startapp signUpLogin

python manage.py makemigrations

python manage.py migrate

python manage.py showmigrations

python manage.py createsuperuser