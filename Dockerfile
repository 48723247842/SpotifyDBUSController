FROM python:3.8-alpine

RUN apk add g++
RUN apk add alpine-sdk
RUN apk add build-base
RUN apk add linux-headers
RUN apk add autoconf
RUN apk add musl-dev
RUN apk add python3-dev
RUN apk add py3-dbus
RUN apk add automake

# RUN apk add ca-certificates
# RUN update-ca-certificates

RUN pip install -U pip

RUN pip install redis
RUN pip install sanic

COPY python_app /home/python_app
WORKDIR "/home/python_app"
ENTRYPOINT [ "python" , "server.py" ]