import msvcrt


def read_key():
    key = msvcrt.getwch()
    if key in ("\x00", "\xe0"):
        msvcrt.getwch()
        return ""
    return key.lower()


def wait_key():
    read_key()
