FROM python:3.7

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev
COPY . .
CMD ["gunicorn", "sib.wsgi:application", "--bind", "0:8000" ] 
