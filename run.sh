PROJECT_NAME="trusted-search"

stop_docker() {
    echo "Stopping Docker resources for project: $PROJECT_NAME"

    # Bring down the Docker Compose project and remove volumes and orphans
    docker compose -p "$PROJECT_NAME" down --volumes --remove-orphans || true

    # Prune containers, volumes, and networks associated with the project
    echo "Pruning Docker resources..."
    docker container prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME" || true
    docker volume prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME" || true
    docker network prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME" || true

    # Flush Celery tasks if applicable
    echo "Flushing Celery tasks..."
    docker compose -p "$PROJECT_NAME" exec -T worker celery -A crawler.crawler_services.celery_manager control purge || true
    docker compose -p "$PROJECT_NAME" exec -T worker celery -A crawler.crawler_services.celery_manager control revoke --terminate --all || true

    # Flush Redis cache if applicable
    echo "Flushing Redis cache..."
    docker compose -p "$PROJECT_NAME" exec -T redis redis-cli FLUSHALL || true

    # Stop all remaining containers related to the project
    echo "Stopping and removing remaining containers..."
    container_names=("trustly-web-mongodb" "trusted-web-elastic" "trusted-web-main" "trusted-web-nginx" "trusted-WEB-redis")
    for container_name in "${container_names[@]}"; do
        if [[ $(docker ps -a --filter "name=$container_name" --format '{{.ID}}') ]]; then
            echo "Removing container: $container_name"
            docker rm -f "$container_name" || true
        fi
    done

    echo "Docker resources for project $PROJECT_NAME have been stopped and cleaned."
}

# Function to build and start the Docker project
start_docker() {
    if [ "$1" == "build" ]; then
        echo "Building Docker project: $PROJECT_NAME"
        docker compose -p "$PROJECT_NAME" build || true
    fi

    echo "Starting Docker project: $PROJECT_NAME"
    docker compose -p "$PROJECT_NAME" up -d || true
    echo "Docker project $PROJECT_NAME is now running."
}

# Main execution
if [ "$1" == "stop" ]; then
    stop_docker
    echo "Crawler service stopped."
else
    stop_docker
    start_docker "$1"
    echo "Crawler service started."
fi
