FROM ubuntu:16.04

RUN apt-get clean && apt-get update && \
    apt-get install -y python3-pip

RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN pip3 install -r requirements.txt

CMD python3 manage.py runserver
