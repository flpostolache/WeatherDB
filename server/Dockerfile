FROM python:3.8

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install flask_expects_json
RUN pip3 install mysql-connector-python

COPY *.py /server/
WORKDIR /server

EXPOSE 6000

ENTRYPOINT ["python3", "server.py"]