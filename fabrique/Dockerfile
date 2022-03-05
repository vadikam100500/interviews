FROM python:3.9

WORKDIR /app
COPY ./poetry.lock ./pyproject.toml ./
RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev
COPY . .
CMD ./manage.py migrate --noinput && \
    ./manage.py collectstatic --no-input && \
    ./manage.py create_admin && \
    gunicorn notification_service.wsgi:application --bind 0:8000 
