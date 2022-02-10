# Sibdev test
- Start 08.02.22 15.00
- End 10.02.22 16.00

## Functionality
- Service with 1 endpoint, working whith GET, POST requests
- On GET return cached data of 5 best clients(by total spent)
- On POST taking csv file and create data from it.

## What used by TOR
- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Local deploy:
    Create file .env and set secrets like in .env.example:
    ```sh
    SECRET_KEY=YOUR_SECRET_KEY
    DEBUG=TRUE # if you want to work in dev
    ALLOWED_HOSTS=host1, host2, etc 

    DJANGO_SUPERUSER_USERNAME=admin # set instead admin, username of superuser
    DJANGO_SUPERUSER_EMAIL=admin@gmail.com # set instead admin@gmail.com, email of superuser
    DJANGO_SUPERUSER_PASSWORD=admin # set instead admin, password of superuser

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres # set instead postgres, name of db
    POSTGRES_USER=postgres # set instead postgres, nikname of superuser of db
    POSTGRES_PASSWORD=postgres # set instead postgres, password of db
    DB_HOST=db # you can rename it or set a needed host, but before make changes to docker-compose.yaml
    DB_PORT=5432
    ```
+ [Install docker ](https://docs.docker.com/get-docker/)
+ If you don't need any files or dirs in container, you can set them in .dockerignore
+ In dir with project run:
    ```sh
    $ docker-compose up
    ```
+ Open a new window of terminal and from dir of project run:
    ```sh
    $ docker-compose exec web ./manage.py migrate --noinput
    $ docker-compose exec web ./manage.py collectstatic --no-input 
    $ docker-compose exec web ./manage.py create_admin
    ```
+ You can get admin panel in http://localhost/admin/ with username and password, that you set in .env (DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD)
+ Work endpoint: http://localhost/deals/

## TOR
- Full tor you can find in [ТЗ] Junior Python.docx file
