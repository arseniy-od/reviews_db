# YAMDB

1. To start project with docker-compose:
```
docker-compose up
```
This will start nginx+gunicorn server.
2. To add data to database you should at first change locale
to support cyrillic symbols:
```bash
docker exec -it db bash

root@<db_container_id>:/# dpkg-reconfigure locales
```
Choose ru_RU.UTF-8. 

3. Create database for storing your data:
```
docker exec -it db psql -U yamdb_user

yamdb_user=# create database yamdb;
```
4. Run migrations:
```bash
docker exec python manage.py migrate
```
5. Prepare database for data transfer from json file, then load data:
```bash
docker exec -it web python manage.py shell

>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

docker exec web python manage.py loaddata sqlite_data.json
```
---
## Superuser creation
There is already superuser in database with credentials:

- email: admin@mail.com
- password: admin

You can delete this user with django ORM and create new one:
```
docker exec -it web python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all().delete()
>>> quit()
```
```
docker exec -it web python manage.py createsuperuser
```
---
API documentation is accessible via index page of yamdb site