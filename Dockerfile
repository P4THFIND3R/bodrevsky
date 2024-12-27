FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

RUN pip install poetry
COPY ../pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY .. /app

EXPOSE 8080

CMD ["python", "-m", "src.main"]