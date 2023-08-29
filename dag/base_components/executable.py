from abc import abstractmethod


class Executable:

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def finish(self):
        raise NotImplementedError
