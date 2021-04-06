FROM python:3.7-alpine

MAINTAINER Numan Ibn Mazid <http://github.com/NumanIbnMazid>

EXPOSE 8000

RUN apk -U upgrade

RUN apk add --update alpine-sdk

RUN apk add --no-cache gcc python3-dev musl-dev libffi-dev openssl-dev rust cargo

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && pip install --no-cache-dir cryptography \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && pip install psycopg2-binary \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk del build-deps libressl-dev musl-dev libffi-dev

ADD . /b2c_admin

WORKDIR /b2c_admin

# RUN python -m pip install --upgrade pip

# RUN pip install Pillow

# RUN pip install cryptography

# RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip freeze > requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]