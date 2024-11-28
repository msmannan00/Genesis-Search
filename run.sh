PROJECT_NAME="trusted-search"
stop_docker() {
    docker compose stop
    docker cp static/. trusted-web-main:/app/static/
    docker cp trustly/templates/. trusted-web-main:/app/trustly/templates/
    container_names=("trustly-web-mongodb" "trusted-web-elastic" "trusted-web-main" "trusted-web-nginx")

    for container_name in "${container_names[@]}"; do
        if [[ $(docker ps -a --filter "name=$container_name" --format '{{.ID}}') ]]; then
            docker rm -f "$container_name"
        fi
    done
}

stop_docker
if [ "$1" == "stop" ]; then
    echo "crawler service stopped"
else
    if [ "$1" == "build" ]; then
        download_and_extract_model
        docker compose -p $PROJECT_NAME build
    fi

    docker compose -p $PROJECT_NAME up -d
    echo "crawler service started"
fi

