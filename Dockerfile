FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV APPLICATION production

WORKDIR /app

ADD . /app

COPY ./requirements.txt ./app

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["./_scripts/build.sh"]
