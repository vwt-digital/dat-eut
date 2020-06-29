FROM python:3.7-slim

WORKDIR /workspace

RUN pip install virtualenv
COPY docker-eac.sh /usr/local/bin/
ADD coverage /
ENTRYPOINT ["docker-eac.sh"]
