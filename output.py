# export csv/json


def format_item(item: dict, index: int) -> str:
    return (
        f"[{index}] {item["title"]}\n"
        f"    likes: {item.get("likes", 0)}\n"
        f"    created_at: {item.get("created_at")}\n"
        f"    url: {item["url"]}\n"
    )


def output(data: list[dict]) -> None:
    print("\n=======result========\n")

    for i, item in enumerate(data, 1):
        print(format_item(item, i))
