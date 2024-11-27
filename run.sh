#!/bin/bash


remove_services() {
    read -p "Are you sure you want to remove all services? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose down --volumes
        docker compose rm -f
    else
        echo "Operation aborted. Services will not be removed."
        exit 1
    fi
}

copy_files() {
    docker compose exec web rm -rf /staticfiles/*
    docker compose exec web rm -rf /static/*
    docker cp static/. trusted-web-main:/app/static/
    docker cp trustly/templates/. trusted-web-main:/app/trustly/templates/
    docker compose exec web python manage.py collectstatic --noinput
}

remove_conflicting_containers() {
    container_names=("trustly-web-mongodb" "trusted-web-elastic" "trusted-web-main" "trusted-web-nginx")

    for container_name in "${container_names[@]}"; do
        if [[ $(docker ps -a --filter "name=$container_name" --format '{{.ID}}') ]]; then
            echo "Stopping and removing conflicting container: $container_name"
            docker rm -f "$container_name"
        fi
    done
}

if [ "$1" == "build" ]; then
    remove_services
    remove_conflicting_containers
    docker compose build --no-cache
    docker compose up -d
    sleep 2
    copy_files
    echo "search service started"
elif [ "$1" == "stop" ]; then
    docker compose down
    remove_conflicting_containers
    echo "services stopped successfully."
elif [ "$1" == "reload_cache" ]; then
    copy_files
    docker stop trusted-web-main
    docker start trusted-web-main
    echo "cache reloaded successfully."
else
    docker compose down
    remove_conflicting_containers
    docker compose up -d
    sleep 2
    copy_files
    echo "search service started"
fi
