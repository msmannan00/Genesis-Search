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

if [ "$1" == "build" ]; then
    docker-compose down
    docker system prune -a --volumes -f
    download_file
    docker-compose build --no-cache
    docker-compose up
else
    docker-compose down
    download_file
    docker-compose up
fi
