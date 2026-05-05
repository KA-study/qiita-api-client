import math
from datetime import datetime

from data_storage.scheme import ActivityData, ActivityMap, ActivityItem
from config import TAU, SECONDS_PER_DAY

def calc_tag_score(tags_logs: ActivityMap, tags: list[str]) -> float:
    #記事に一つもtagが付されていないとき
    #本当に0.0を返してよいのか。後ほど要検討
    if not tags:
        return 0.0

    #tags_logsが空だった（一度もtag指定で検索したことがない）とき
    all_count: int = sum(tags_logs[tag_name]["count"] for tag_name in tags_logs)
    if not all_count:
        return 0.0

    score_list = []
    now = datetime.now()

    for tag in tags:

        #tags_logsにarticleのtagが含まれているとは限らない
        if tag not in tags_logs:
            continue

        #json書き込み失敗時、また後程manage_params()などを拡張したときに、last_usedがNoneのまま通ってくる可能性をカット
        if not tags_logs[tag]["last_used"]:
            continue

        count: int = tags_logs[tag]["count"] 
        last_used = datetime.fromisoformat( tags_logs[tag]["last_used"] )

        elapsed_day = (now - last_used).total_seconds() / SECONDS_PER_DAY
        
        score_list.append((count/all_count)*math.exp(-elapsed_day/TAU)) 

    #記事にtagが付されていて、かつtags_logsもからでないが、tags_logsにあてはまるtagが一つもなかった時。
    if not score_list:
        return 0.0   

    #スコアリングで、最大値以外すべて無視している。後ほど要再設計。
    return max(score_list) 

def calc_keyword_score() -> int:

def calc_sort_score() -> int:

def calc_score_closure():
    cache = {}

    def calc_article_score(
            logs: ActivityData, article:dict, sort: str
            ) -> float:
        
        return (
            calc_tag_score(logs["tags"], article["tags"]) +
            calc_keyword_score() +
            calc_sort_score()
        )

    return calc_article_score