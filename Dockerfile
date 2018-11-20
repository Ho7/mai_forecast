FROM ubuntu:16.04

RUN apt-get clean && \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:jonathonf/python-3.6 && \
    apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip && \
    apt-get install -y locales

RUN ln -fs /usr/bin/python3.6 /usr/bin/python3
RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN pip3 install django==2.1 \
                 djangorestframework==3.8.2 \
                 requests

COPY . /opt/forecast
WORKDIR /opt/forecast
CMD python3 manage.py runserver 0.0.0.0:8000