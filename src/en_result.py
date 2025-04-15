from enum import IntFlag, auto

class Result(IntFlag):
    INIT_SUCCESS = auto()
    INIT_REDUNDANT = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_REDUNDANT = auto()
    LOGIN_FAILED = auto()
    LOGOUT_SUCCESS = auto()
    LOGOUT_REDUNDANT = auto()
    RESET_SUCCESS = auto()
    SERVICE_LIST = auto()
    SERVICE_ADDED = auto()
    SERVICE_REMOVED = auto()
    SERVICE_UPDATED = auto()
    SERVICE_ADDED_FAILED = auto()
    SESSION_INACTIVE = auto()

    def __str__(self):
        messages = [RESULT_MESSAGES[flag] for flag in Result if flag in self]
        return "\n".join(f"[{flag.name}] {RESULT_MESSAGES[flag]}" for flag in Result if flag in self)


RESULT_MESSAGES = {
    Result.INIT_SUCCESS: "Enpass has been initialized.",
    Result.INIT_REDUNDANT: "Already initialized enpass. Please reset before reinitializing.",
    Result.LOGIN_SUCCESS: "Logged into enpass account.",
    Result.LOGIN_REDUNDANT: "Already logged in to enpass.",
    Result.LOGIN_FAILED: "Login unsuccessful. Please try again.",
    Result.LOGOUT_SUCCESS: "Logged out of enpass account.",
    Result.LOGOUT_REDUNDANT: "Already logged out of enpass.",
    Result.RESET_SUCCESS: "Enpass has been reset.",
    Result.SERVICE_LIST: "Here is the list of services.",
    Result.SERVICE_ADDED: "Service has been added.",
    Result.SERVICE_REMOVED: "Service has been removed.",
    Result.SERVICE_UPDATED: "Service has been updated.",
    Result.SERVICE_ADDED_FAILED: "Service has not been added.",
    Result.SESSION_INACTIVE: "Please login and try again.",
}
