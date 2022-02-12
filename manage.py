#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from modules.user_data_parser.parse_instance.parse_controller.parse_controller import parse_controller
from modules.user_data_parser.parse_instance.parse_controller.parse_enums import PARSE_COMMANDS

import os
import sys
import threading

def __init_user_data_parser():
    parse_controller.get_instance().invoke_trigger(PARSE_COMMANDS.S_START_PARSER)

def main():
    threading.Thread(target=__init_user_data_parser).start()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Genesis.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError() from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
