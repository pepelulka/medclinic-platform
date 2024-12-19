FROM python:3.10-slim

RUN apt-get update
RUN apt install -y curl

RUN curl -fsSL \
    https://raw.githubusercontent.com/pressly/goose/master/install.sh |\
    sh

WORKDIR ./app

COPY ./requirements.txt ./requirements.txt
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
COPY ./src ./src

RUN pip install -r requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "main:app"]
