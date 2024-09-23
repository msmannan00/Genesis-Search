#!/bin/bash

if [ "$1" == "build" ]; then
    docker-compose down
    docker system prune -a --volumes -f
    docker-compose build --no-cache
    docker-compose up
else
    docker-compose down
    docker-compose up
fi
