#!/bin/bash

cd docker-compose

docker-compose down --volumes

docker volume rm docker-compose_db_data

docker rmi my-server:latest adminer:latest mysql:5.7 python:3.8

sudo rm -rf ./database/data
