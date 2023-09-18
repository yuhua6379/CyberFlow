from abc import abstractmethod
from enum import Enum


class Status(Enum):
    SUCCESS = 0
    FAIL = 1


class Executable:

    def __init__(self):
        self._finish = False
        self._status = None
        self._exception = None

    def execute_not_finish(self):
        if self.finish():
            raise RuntimeError("try to execute a finished element")
        self.execute()

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def set_finish(self):
        self._finish = True

    def set_status(self, status: Status):
        self._status = status

    def set_exception(self, exception: Exception):
        self._exception = exception

    def finish(self):
        return self._finish

    def status(self):
        return self._status

    def exception(self):
        return self._exception
