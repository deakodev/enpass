from enum import IntFlag, auto


class Result(IntFlag):
    INIT_SUCCESS = auto()
    INIT_FAILED = auto()
    INIT_REDUNDANT = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_REDUNDANT = auto()
    LOGIN_FAILED = auto()
    LOGOUT_SUCCESS = auto()
    LOGOUT_REDUNDANT = auto()
    SERVICE_LIST = auto()
    SERVICE_LIST_FAILED = auto()
    SERVICE_ADDED = auto()
    SERVICE_ADDED_FAILED = auto()
    SERVICE_REMOVED = auto()
    SERVICE_REMOVED_FAILED = auto()
    SERVICE_VIEW = auto()
    SERVICE_VIEW_FAILED = auto()
    SESSION_INACTIVE = auto()

    def __str__(self):
        return "\n".join(f"[{flag.name}] {RESULT_MESSAGES[flag]}" for flag in Result if flag in self)


RESULT_MESSAGES = {
    Result.INIT_SUCCESS: "Enpass has been initialized.",
    Result.INIT_FAILED: "Enpass was not initialized.",
    Result.INIT_REDUNDANT: "Enpass already initialized. Please reset before reinitializing.",
    Result.LOGIN_SUCCESS: "Logged into enpass account.",
    Result.LOGIN_REDUNDANT: "Already logged in to enpass.",
    Result.LOGIN_FAILED: "Login unsuccessful. Please try again.",
    Result.LOGOUT_SUCCESS: "Logged out of enpass account.",
    Result.LOGOUT_REDUNDANT: "Already logged out of enpass.",
    Result.SESSION_INACTIVE: "Please login and try again.",
    Result.SERVICE_LIST: "A list of all your services.",
    Result.SERVICE_LIST_FAILED: "Unable to list services.",
    Result.SERVICE_ADDED: "Service has been added.",
    Result.SERVICE_ADDED_FAILED: "Service has not been added.",
    Result.SERVICE_REMOVED: "Service has been removed.",
    Result.SERVICE_REMOVED_FAILED: "Service was not removed.",
    Result.SERVICE_VIEW: "Service has been viewed",
    Result.SERVICE_VIEW_FAILED: "Service cannot be viewed.",
}
