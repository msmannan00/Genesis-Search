import os
import sys

from app_manager.elastic_manager.elastic_enums import ELASTIC_CONNECTIONS
from app_manager.mongo_manager.mongo_enums import MONGO_CONNECTIONS

def main():

    MONGO_CONNECTIONS.S_MONGO_DATABASE_IP = "localhost"
    MONGO_CONNECTIONS.S_MONGO_USERNAME = ""
    MONGO_CONNECTIONS.S_MONGO_PASSWORD = ""
    ELASTIC_CONNECTIONS.S_ELASTIC_USERNAME = ""
    ELASTIC_CONNECTIONS.S_ELASTIC_PASSWORD = ""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trustly.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError() from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
