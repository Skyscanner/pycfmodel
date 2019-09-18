from .regexs import FIRST_CAP, ALL_CAP


def convert_to_snake_case(name):
    s1 = FIRST_CAP.sub(r'\1_\2', name)
    return ALL_CAP.sub(r'\1_\2', s1).lower()
