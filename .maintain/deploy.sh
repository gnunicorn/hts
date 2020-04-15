#!/bin/bash
set -e

docker-compose build
docker-compose stop hts-app
docker-compose up -d