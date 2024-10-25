FROM python:3.11.10

RUN apt update && apt install -y \
    curl \
    make \
    iputils-ping \
    libmediainfo-dev \
    libgl1-mesa-glx

WORKDIR /app

COPY . .

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry install

CMD ["make", "run"]
