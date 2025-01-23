FROM node:latest

WORKDIR /root

COPY ./frontend ./frontend

WORKDIR /root/frontend

RUN npm install

ENTRYPOINT [ "npm" ]
CMD [ "run", "dev" ]
