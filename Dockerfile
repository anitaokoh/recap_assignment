FROM python:3.8-slim

WORKDIR /data_manipulation

COPY  *.py requirements.txt Makefile   /data_manipulation/



RUN apt update && apt install -y make 

RUN chmod -R +x *.py requirements.txt Makefile && make install
RUN mkdir data


