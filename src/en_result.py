from enum import Enum, auto

class Result(Enum):
    EN_NONE = auto()
    EN_OK = auto()
    EN_ERROR = auto()
    INIT_SUCCESS = "Enpass has been initialized."
    INIT_REDUNDANT = "Already initialized enpass. Please reset before reinitializing."
    LOGIN_SUCCESS = "Logged into enpass account."
    LOGIN_FAILED = "Login unsuccessful. Please try again."

    def __str__(self):
        return f"[{self.name}] {self.value}"