from enum import Enum

URL = "https://qiita.com/api/v2/items"

TAG_DEFAULT = "python"
KEYWORD_DEFAULT = ""
QUERY_DEFAULT = ""
SORT_DEFAULT = "created_at"
PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 10


class SortOption(Enum):
    # 第一引数と第二引数はそのまま展開されて__init__に渡される。
    CREATED_AT = ("created_at", True)  # (key, is_api_supported)
    UPDATED_AT = ("updated_at", True)
    LIKES = ("likes", True)
    STOCKS = ("stocks", True)

    TITEL_LENGTH = ("title_length", False)
    TAG_COUNT = ("tag_count", False)

    def __init__(self, key: str, is_api_supported: bool):
        self.__key = key
        self.__is_api_supported = is_api_supported

    @property
    def key(self) -> str:
        return self.__key

    @property
    def is_api_supported(self) -> bool:
        return self.__is_api_supported

    # 定数として扱うため、setterはつけない。
