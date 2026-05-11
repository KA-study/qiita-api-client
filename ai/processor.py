import re
from storage.scheme import ArticleData
from ai.class_manager import AIArticleData


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


def normalize_for_ai(data: ArticleData) -> AIArticleData:
    ai_data: AIArticleData = {
        "id": "",
        "title": "",
        "body": "",
        "tags": [],
    }

    ai_data["id"] = data["id"]
    ai_data["title"] = data["title"]
    ai_data["body"] = normalize_body(data["body"])
    ai_data["tags"] = data["tags"]

    return ai_data
