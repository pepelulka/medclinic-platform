FROM python:3.10-slim

RUN apt-get update
RUN apt install -y curl

RUN curl -fsSL \
    https://raw.githubusercontent.com/pressly/goose/master/install.sh |\
    sh

WORKDIR /root/app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
COPY ./src ./src


ENTRYPOINT ["./docker-entrypoint.sh"]
CMD [ "/root/app/src", "uvicorn", "main:app", "--host", "0.0.0.0" ]
