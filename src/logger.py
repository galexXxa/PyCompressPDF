import os

VERBOSE = False

def log(message):

    if VERBOSE:
        print(message)

def info(message):

    print(message)

def debug(message):

    if VERBOSE:
        print(
            "[DEBUG]",
            message
        )

def success(message):

    print(
        "[OK]",
        message
    )

def error(message):

    print(
        "[ERROR]",
        message
    )