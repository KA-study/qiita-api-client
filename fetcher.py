# fetch qiita articles
import requests
from abc import ABC, abstractmethod


class FetchClientAbstract(ABC):
    @abstractmethod
    def fetch(self, params: dict) -> list | dict:
        pass


# 具象クラスを増やす場合は、以下のことに注意すること。
# ・同じ意味のデータを返すか。
# ・同じ前提条件で動くか。
# ・例外の扱いが一致しているか。
class QiitaClient(FetchClientAbstract):
    def __init__(self, url):
        self.__url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value

    def fetch(self, params: dict) -> list[dict]:

        try:
            res = requests.get(self.__url, params=params, timeout=10)
            res.raise_for_status()

            # for debug
            # print(res.url)

            return res.json()
        except requests.exceptions.Timeout:
            raise RuntimeError("Request timeout")
        except requests.exceptions.HTTPError as ex:
            raise RuntimeError(f"HTTP error: {ex}")
        except ValueError:
            raise RuntimeError("Invalid JSON response")
