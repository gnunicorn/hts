#!/bin/bash
set -e

docker-compose build
docker-compose run hts-app migrate
docker-compose stop hts-app hts-worker
docker-compose up -d