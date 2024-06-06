import re


def safename(name: str, lower=False):
    name = (re.sub(r"[0-9\.\(\)]", "", name)
            .replace(" ", "_")
            .replace("%", "percent"))
    if lower:
        name = name.lower()
    return name


datetime_regex = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
