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
    # Info Logs
    def i(self, p_log):
        print(colored(p_log, 'cyan'))

    # Info Logs
    def s(self, p_log):
        print(colored(p_log, 'green'))

    def w(self, p_log):
        print(colored(p_log, 'yellow'))

    # Error Logs
    def e(self, p_log):
        print(colored(p_log, 'red'))