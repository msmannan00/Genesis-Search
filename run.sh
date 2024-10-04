#!/bin/bash

URL="https://drive.usercontent.google.com/download?id=1LTI94WsJbf8PheaMb7269Vxm5ZKtbHwb&export=download&authuser=0&confirm=t&uuid=1163171e-ce7c-4a98-9a46-2a3ce2a91f48&at=AO7h07dQiPcuFN56QrmDruowdk0P%3A1727101003781"
DEST_DIR="static/trustly/.well-known/model"
DEST_FILE="$DEST_DIR/toxic-model.zip"

mkdir -p $DEST_DIR

download_file() {
    if [ -f "$DEST_FILE" ]; then
        echo "File $DEST_FILE already exists. Skipping download."
    else
        if curl --output /dev/null --silent --head --fail "$URL"; then
            echo "Downloading file..."
            curl -# -L "$URL" -o "$DEST_FILE"
        else
            echo "Error: Invalid Model URL or network issue."
            exit 1
        fi
    fi
}

remove_services() {
    read -p "Are you sure you want to remove all services? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down --volumes
        docker-compose rm -f
    else
        echo "Skipping service removal."
        exit 1
    fi
}

copy_files() {
    docker-compose exec web rm -rf /staticfiles/*
    docker-compose exec web rm -rf /static/*
    docker cp static/. trusted-web-main:/app/static/
    docker-compose exec web python manage.py collectstatic --noinput
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
    download_file
    remove_conflicting_containers
    docker-compose build --no-cache
    copy_files
    docker-compose up
else
    docker-compose down
    remove_conflicting_containers
    download_file
    copy_files
    docker-compose up
fi
