#!/usr/bin/env python
import os
import sys
import threading

from genesis_modules.user_data_parser.parse_instance.parse_controller.parse_controller import parse_controller
from genesis_modules.user_data_parser.parse_instance.parse_controller.parse_enums import PARSE_COMMANDS
from genesis_shared_directory.log_manager.log_controller import log
from genesis_shared_directory.state_manager.server_status import SERVER_STATUS
from genesis_shared_directory.state_manager.strings import MESSAGE_STRINGS


def __init_server_state():
    if "S_SERVER_STATE" in os.environ:
        if os.environ['S_SERVER_STATE'] == "dev" or os.environ['S_SERVER_STATE'] == "production_server_1" or os.environ['S_SERVER_STATE'] == "production_server_2":
            SERVER_STATUS.S_SERVER_STATE = os.environ['S_SERVER_STATE']
        else:
            log.g().e(MESSAGE_STRINGS.S_ENVIORNMENTAL_VARIABLE_INVALID_ERROR)
            exit(0)
    else:
        log.g().e(MESSAGE_STRINGS.S_ENVIORNMENTAL_VARIABLE_ERROR)
        exit(0)

def __init_user_data_parser():
    parse_controller.get_instance().invoke_trigger(PARSE_COMMANDS.S_START_PARSER)

def main():
    threading.Thread(target=__init_user_data_parser).start()
    __init_server_state()

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
