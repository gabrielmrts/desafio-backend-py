#!/bin/bash

run_docker_compose() {
    docker compose up -d
}

run_tests() {
    docker compose exec -it app ./start.sh tests
}

down_docker_compose() {
	docker-compose -f docker-compose.yml down
}

if [ "$1" == "up" ]; then
    run_docker_compose
elif [ "$1" == "tests" ]; then
    run_tests
elif [ "$1" == "down" ]; then
    down_docker_compose
else
    echo "Usage: $0 {up|tests|down}"
fi
