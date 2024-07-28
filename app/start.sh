#!/bin/bash

install_dependencies () {
	echo "Installing dependencies ... "
	pip install -r requirements.txt -q
}

start() {
	echo "Starting Api..."
	## install the dependencies
	install_dependencies
    # Run the migrations
    cd app
    alembic upgrade head
    cd ..
    # On development environment let the automatic reload working
    fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload
}

run_migration() {
    cd app
    alembic revision --autogenerate -m "$1"
}

run_tests() {
    pytest
}

environment_down() {
	docker-compose -f ../docker-compose.yml down
}

rebuild_environment() {
	echo "Rebuilding envivonment ..."
	docker-compose -f ../docker-compose.yml down && docker-compose -f ../docker-compose.yml up -d --force-recreate
	echo "---------------------------------------"
	echo "Setting up database defintions ..."
    cd app
	alembic upgrade head
}

start_environment() {
	# Start environment without recreating containers #
	echo "Starting envivonment..."
	docker-compose -f ../docker-compose.yml up -d
	start
}

if [ "$1" == "dev" ]; then
	start
elif [ "$1" == "tests" ]; then
	run_tests $2
elif [ "$1" == "env_down" ]; then
	environment_down
fi
