#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

'''
def __init_state_manager():
    while True:
        try:
            requests.get("https://boogle.store/app_status", timeout=10)
            log.g().i("alive status sent")
        except Exception as ex:
            log.g().e("alive status sent failed : " + str(ex))
        sleep(60)
'''

def main():
    # threading.Thread(target=__init_state_manager).start()
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
