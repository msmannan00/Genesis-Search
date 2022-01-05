import datetime

from termcolor import colored


class log:

    __instance = None

    # Initializations
    @staticmethod
    def g():
        if log.__instance is None:
            log()
        return log.__instance

    def __init__(self):
        log.__instance = self

    # Info Logs
    def i(self, p_log):
        print(colored(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " : " + p_log, 'cyan'))

    # Success Logs
    def s(self, p_log):
        print(colored(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " : " + p_log, 'green'))

    # Warning Logs
    def w(self, p_log):
        print(colored(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " : " + p_log, 'yellow'))

    # Error Logs
    def e(self, p_log):
        print(colored(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " : " + p_log, 'red'))
