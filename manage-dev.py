import os
import sys
import requests
from pymongo import MongoClient
from trustly.services.elastic_manager.elastic_enums import ELASTIC_CONNECTIONS
from trustly.services.mongo_manager.mongo_enums import MONGO_CONNECTIONS


def check_elasticsearch():
    try:
        response = requests.get("http://localhost:9200", timeout=5)
        if response.status_code != 200:
            sys.exit(1)
    except requests.exceptions.RequestException:
        sys.exit(1)


def check_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
    except Exception:
        sys.exit(1)


def main():
    MONGO_CONNECTIONS.S_MONGO_DATABASE_IP = "localhost"
    MONGO_CONNECTIONS.S_MONGO_USERNAME = ""
    MONGO_CONNECTIONS.S_MONGO_PASSWORD = ""
    ELASTIC_CONNECTIONS.S_ELASTIC_USERNAME = ""
    ELASTIC_CONNECTIONS.S_ELASTIC_PASSWORD = ""

    check_elasticsearch()
    check_mongodb()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trustly.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Couldn't import Django. Make sure it's installed and available on your PYTHONPATH.")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
