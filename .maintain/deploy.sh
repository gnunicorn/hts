#!/bin/bash
set -e

docker-compose build
docker-compose run hts-app migrate
docker-compose stop hts-app
docker-compose up -d