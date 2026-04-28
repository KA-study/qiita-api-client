# fetch qiita articles
import requests
from config import URL


def fetcher(params: dict) -> list | dict:

    try:
        res = requests.get(URL, params=params, timeout=10)
        res.raise_for_status()

        print(res.url)

        return res.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timeout")
    except requests.exceptions.HTTPError as ex:
        raise RuntimeError(f"HTTP error: {ex}")
    except ValueError:
        raise RuntimeError("Invalid JSON response")
