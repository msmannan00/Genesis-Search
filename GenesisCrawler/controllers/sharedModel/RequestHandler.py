from abc import abstractmethod


class RequestHandler:

    @abstractmethod
    def invoke_trigger(self, p_command, p_data):
        pass
