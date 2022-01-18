#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

from modules.user_data_parser.parse_instance.parse_controller.parse_controller import parse_controller
from modules.user_data_parser.parse_instance.parse_controller.parse_enums import PARSE_COMMANDS

def __init_user_data_parser():
    parse_controller.get_instance().invoke_trigger(PARSE_COMMANDS.S_START_PARSER)

def __init_user_data_parser():
    parse_controller.get_instance().invoke_trigger(PARSE_COMMANDS.S_START_PARSER)

def main():
    threading.Thread(target=__init_user_data_parser).start()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
