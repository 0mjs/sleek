import re


def path_matcher(path: str) -> str:
    pattern = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
    return re.compile(f"^{pattern}$")
