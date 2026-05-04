import math
from datetime import datetime

from data_storage.scheme import ActivityData, ActivityMap, ActivityItem
from config import TAU, SECONDS_PER_DAY

def calc_tag_score(tags_logs: ActivityMap, tag: str) -> float:
    tag_score = 0

    #記事に一つもtagが付されていないとき
    if tag is None or tag == "":
        ...

    #logsを初期化するときに、（存在するのであれば、つまり上の分岐に引っかからないのであれば以下は成り立つ
    all_count: int = sum(tags_logs[tag_name]["count"] for tag_name in tags_logs)
    count: int = tags_logs[tag]["count"]
    last_used = datetime.fromisoformat( tags_logs[tag]["last_used"] )

    now = datetime.now()

    delta = now - last_used
    elapsed_day = delta.total_seconds() / SECONDS_PER_DAY
    
    return (count/all_count)*math.exp(-elapsed_day/TAU) 

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