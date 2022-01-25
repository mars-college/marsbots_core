# syntax=docker/dockerfile:1
FROM python:3.9-buster AS python
WORKDIR /bots
ENV FLIT_ROOT_INSTALL=1
COPY . .
RUN pip install flit
RUN python -m flit install --pth-file

RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g pm2@latest

RUN chmod +x run.sh
RUN cp run.sh /tmp

ENTRYPOINT ["/tmp/run.sh"]
