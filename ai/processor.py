import re


def normalize_body(body: str) -> str:

    # image
    body = re.sub(r"!\[.*?\]\(.*?\)", "[IMAGE]", body)

    # html
    body = re.sub(r"<[^>]+>", "", body)

    # url
    body = re.sub(r"https?://\S+", "[URL]", body)

    # multiple blank lines
    body = re.sub(r"\n{3,}", "\n\n", body)

    return body.strip()
