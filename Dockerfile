# syntax=docker/dockerfile:1
FROM python:3.9-buster AS python
WORKDIR /bots
COPY marsbots_core marsbots_core
COPY bot.py bot.py
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY entrypoint.sh entrypoint.sh
ENV FLIT_ROOT_INSTALL=1

# RUN pip install flit
# RUN python -m flit install --pth-file

# RUN apt-get update && apt-get install -y nodejs npm
# RUN npm install -g pm2@latest

RUN chmod +x entrypoint.sh
RUN cp entrypoint.sh /tmp

ENTRYPOINT ["/tmp/entrypoint.sh"]
