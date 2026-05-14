import re
import hashlib

from storage.scheme import ArticleData
from ai.definitions import(
    AIArticleData
)


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


def hash_body(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def normalize_for_ai(data: ArticleData) -> AIArticleData:
    ai_data: AIArticleData = {
        "data_type": "article",
        "id": "",
        "title": "",
        "body": "",
        "tags": [],
        "hash_value": "",
    }

    ai_data["id"] = data["id"]
    ai_data["title"] = data["title"]
    ai_data["body"] = normalize_body(data["body"])
    ai_data["tags"] = data["tags"]
    ai_data["hash_value"] = hash_body(data["body"])

    return ai_data