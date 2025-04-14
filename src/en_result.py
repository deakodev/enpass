from enum import Enum, auto

class Result(Enum):
    INIT_SUCCESS = "Enpass has been initialized."
    INIT_REDUNDANT = "Already initialized enpass. Please reset before reinitializing."
    LOGIN_SUCCESS = "Logged into enpass account."
    LOGIN_REDUNDANT = "Already logged in to enpass."
    LOGIN_FAILED = "Login unsuccessful. Please try again."
    LOGOUT_SUCCESS = "Logged out of enpass account."

    def __str__(self):
        return f"[{self.name}] {self.value}"