import re


def slugify(title):
    return re.sub(r"\s+", "-", title.strip())
