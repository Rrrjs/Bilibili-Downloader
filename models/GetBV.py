import re

def get_bv(url):
    pattern = r"\/(BV\w+)"
    match = re.search(pattern, url)
    if match:
        bv = match.group(1)
    else:
        return None
    return bv
def get_p(url):
    match = re.search(r"\?p=(\d+)", url)
    if match:
        numberp = match.group(1)
        return numberp
    else:
        numberp = 1
        return numberp