PROJECT_NAME="trusted-search"
stop_docker() {
    docker compose -p $PROJECT_NAME down --volumes --remove-orphans
    docker container prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME"
    docker volume prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME"
    docker network prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME"
    docker image prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME"
    docker compose -p $PROJECT_NAME exec -T worker celery -A crawler.crawler_services.celery_manager control purge || true
    docker compose -p $PROJECT_NAME exec -T worker celery -A crawler.crawler_services.celery_manager control revoke --terminate --all || true
    docker compose -p $PROJECT_NAME exec -T redis redis-cli FLUSHALL || true

    docker compose stop
    docker cp static/. trusted-web-main:/app/static/
    docker cp trustly/templates/. trusted-web-main:/app/trustly/templates/
    container_names=("trustly-web-mongodb" "trusted-web-elastic" "trusted-web-main" "trusted-web-nginx" "trusted-WEB-redis")

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

