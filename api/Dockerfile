FROM python:3.11

ENV POETRY_VERSION=1.7.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY src/ /app/src/

EXPOSE 8000

CMD ["poetry", "run", "python", "src/docs-retrieval.py"]