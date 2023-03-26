FROM python:3.10

WORKDIR /usr/src/app

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.4.1


ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./backpressure_for_dummies ./backpressure_for_dummies

CMD ["uvicorn", "backpressure_for_dummies.main:app", "--host", "0.0.0.0", "--port", "80"]
