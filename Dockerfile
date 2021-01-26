FROM python:3.6-alpine AS build
COPY . /src
RUN pip install --upgrade pip \
    && pip install wheel
RUN cd /src \
    && python setup.py bdist_wheel -d /deps

FROM python:3.6-alpine
MAINTAINER scielo-dev@googlegroups.com

RUN apk add --update \
    && apk add gcc g++ mariadb-dev \
    && pip install --upgrade pip

COPY . /app
COPY production.ini /app/config.ini
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

WORKDIR /app

RUN pip install -e .

EXPOSE 6543

ENV PYTHONUNBUFFERED 1
ENV MARIADB_STRING_CONNECTION "mysql://user:pass@localhost:port/database"
ENV APPLICATION_URL "http://127.0.0.1:6543"

USER nobody

CMD ["/app/start.sh"]
