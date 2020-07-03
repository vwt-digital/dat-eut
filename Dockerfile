FROM python:3.7-slim

WORKDIR /workspace

RUN pip install virtualenv
RUN pip install --upgrade google-cloud
COPY docker-eac.sh /usr/local/bin/
COPY coverage /coverage
ENTRYPOINT ["docker-eac.sh"]
