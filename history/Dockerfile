FROM python:3.8.3-alpine

WORKDIR /usr/src/history

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/history/entrypoint.sh"]