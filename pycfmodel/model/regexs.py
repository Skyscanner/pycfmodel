import re


FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP = re.compile('([a-z0-9])([A-Z])')
