# syntax=docker/dockerfile:1
FROM python:3.9-buster AS python
WORKDIR /bots
COPY . .
ENV FLIT_ROOT_INSTALL=1

RUN pip install flit
RUN python -m flit install --pth-file

RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g pm2@latest

RUN chmod +x entrypoint.sh
RUN cp entrypoint.sh /tmp

ENTRYPOINT ["/tmp/entrypoint.sh"]
