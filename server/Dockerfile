FROM python:3.8

COPY requirements /requirements_dir/requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements_dir/requirements

ADD *.py /server/
WORKDIR /server

EXPOSE 6000

