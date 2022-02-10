FROM python:3.7

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev
COPY . .
# It is bad practice, better do migration by hands
# In TZ 1 command, ok
CMD ./manage.py migrate --noinput && \
    ./manage.py collectstatic --no-input && \
    ./manage.py create_admin && \
    gunicorn sib.wsgi:application --bind 0:8000 
