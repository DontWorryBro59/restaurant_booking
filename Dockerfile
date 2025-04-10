FROM python:3.12.6-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip --no-cache-dir \
    && pip install poetry --no-cache-dir

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]
