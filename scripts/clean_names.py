
def remove_leading_whitespace(text: str) -> str:
    """
    remove white space at front/back of string
    :param text:
    :return:
    """
    return text.strip()


def replace_and(text: str) -> str:
    """
    replace & with AND to help with naming conventions
    :param text:
    :return:
    """
    return text.replace('&', 'AND')


def remove_double_whitespace(text: str) -> str:
    """
    remove double whitespace string
    :param text:
    :return:
    """
    return " ".join(text.split())


def remove_all_characters(text: str) -> str:
    """
    remove all characters of string
    :param text:
    :return:
    """
    return text.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})


def replace_white_underscore(text: str) -> str:
    """
    remove white
    :param text:
    :return:
    """
    return text.replace(' ', '_')


def replace_double_underscore_with_single(text: str) -> str:
    """
    replace underscores
    :param text:
    :return:
    """
    return text.replace(r"__", "_").replace(r"___", "_")


def remove_double_underscore(text: str) -> str:
    """
    remove double underscores
    :param text:
    :return:
    """
    return text.replace(r"__", "")


def remove_front_underscore(text: str) -> str:
    """
    remove front underscores
    :param text:
    :return:
    """
    prefix = "_"
    return text[len(prefix):] if text.startswith(prefix) else text


def remove_back_underscore(text: str) -> str:
    """
    remove back underscores
    :param text:
    :return:
    """
    prefix = "_"
    return text.rstrip(prefix)


names = ["FCU A & B","Whats up in @ustralia",  "FCU!#!@ 1 Start/Stop", "  FCU 1!@#/A ", "_FCU!@# 1/A ",
         "FCU'1!@", "FCU 1\A ", "__FCU 1\A_ ", "FCU_1_A", "FCU1", "FCUA1_L1_"]
