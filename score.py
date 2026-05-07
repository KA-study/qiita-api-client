import math
from datetime import datetime
import re

from data_storage.scheme import ActivityData, ActivityMap
from config import TAU, SECONDS_PER_DAY


def calc_tag_score(tags_logs: ActivityMap, tags: list[str], now: datetime) -> float:
    # 記事に一つもtagが付されていないとき
    # 本当に0.0を返してよいのか。後ほど要検討
    if not tags:
        return 0.0

    score_list = []

    for tag in tags:

        # tags_logsにarticleのtagが含まれているとは限らない
        if tag not in tags_logs:
            continue

        # json書き込み失敗時、また後程manage_params()などを拡張したときに、last_usedがNoneのまま通ってくる可能性をカット
        if not tags_logs[tag]["last_used"]:
            continue

        count: int = tags_logs[tag]["count"]
        last_used = datetime.fromisoformat(tags_logs[tag]["last_used"])

        elapsed_day = (now - last_used).total_seconds() / SECONDS_PER_DAY

        # この部分の計算メソッドは、countの大きさに大きく依存するため、必要に応じて緩衝するようにメソッドを変更する。
        score_list.append(math.log(1 + count) * math.exp(-elapsed_day / TAU))

    # 記事にtagが付されていて、かつtags_logsもからでないが、tags_logsにあてはまるtagが一つもなかった時。
    if not score_list:
        return 0.0

    # スコアリングで、最大値以外すべて無視している。後ほど要再設計。
    return max(score_list)


def calc_keyword_score(
    keywords_logs: ActivityMap, tags: list[str], title: str, now: datetime
) -> float:
    tokens = {
        "title": [],
        "tags": [],
    }

    if not keywords_logs:
        return 0.0

    # 辞書を回すとkeyが取り出される
    # titleはstrだから部分一致、tagはリストだから完全一致。これで良し。
    for token in keywords_logs.keys():
        if re.search(
            rf"\b{re.escape(token)}\b", title
        ):  # searchメソッドがマッチしなかったときNoneを返すことを利用する
            tokens["title"].append(token)
        if token in tags:
            tokens["tags"].append(token)

    score_dict = {
        "title": [],
        "tags": [],
    }

    for type, tokens_half in tokens.items():

        for token in tokens_half:

            param = keywords_logs[token]

            if not param["last_used"]:
                continue

            last_used = datetime.fromisoformat(param["last_used"])
            elapsed_day = (now - last_used).total_seconds() / SECONDS_PER_DAY

            freq = math.log(1 + param["count"])
            recency = math.exp(-elapsed_day / TAU)

            score_dict[type].append(freq * recency)

    # 最大値以外を無視する処理。後ほど要再設計。
    title_score = max(score_dict["title"]) if score_dict["title"] else 0.0
    tag_score = max(score_dict["tags"]) if score_dict["tags"] else 0.0

    return title_score * 0.7 + tag_score * 0.3

                

def calc_sort_score() -> int:

def calc_score_closure():
    cache = {}

    #logsデータは小文字化済み。残りのデータも小文字化すること。
    def calc_article_score(
            logs: ActivityData, article:dict, sort: str
            ) -> float:

        now = datetime.now()

        #元データを破壊しないように注意
        normalized_tags = [tag.lower() for tag in article["tags"]]
        normalized_title = article["title"].lower()
        
        return (
            calc_tag_score(logs["tags"], normalized_tags, now) +
            calc_keyword_score(logs["keywords"], normalized_tags, normalized_title, now) +
            calc_sort_score()
        )

    return calc_article_score