from termcolor import cprint


def print_green(text: str):
    cprint(text, "green")


def print_red(text: str):
    cprint(text, "red")


def print_yellow(text: str):
    cprint(text, "yellow")


def print_header(text: str):
    cprint(text, "grey", "on_white")
