FROM python:3.7-slim

WORKDIR /workspace

COPY docker-e2e_api_coverage.sh /usr/local/bin/
RUN pip install virtualenv
ENTRYPOINT ["docker-e2e_api_coverage.sh"]
