FROM python:3.11.2

WORKDIR /usr/src/app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

CMD ["poetry", "run", "main-run"]