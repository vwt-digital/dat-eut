FROM python:3.7-slim

WORKDIR /workspace

RUN pip install virtualenv
COPY docker-eac.sh /usr/local/bin/
ENTRYPOINT ["docker-eac.sh"]
