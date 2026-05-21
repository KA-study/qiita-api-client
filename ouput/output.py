# export csv/json
from datetime import datetime

from storage.scheme import ArticleData
from ai.definitions import AIProcessedData


def format_ai_processed(ai: AIProcessedData | None) -> str | None:
    if ai is None:
        return None
    
    return (
        f"    ai_summary: {ai.ai_output.summary}\n"
        f"    ai_level: {ai.ai_output.audience_level}\n"
        f"    ai_cost: {ai.ai_metadata.used_total_tokens}\n"
    )

def format_item(item: ArticleData, index: int) -> str:
    created_at = item.get("created_at")    
    if not created_at:
        raise ValueError(f"the created_at {item['title']} is unclear")

    lines = [
        f"[{index}] {item['title']}\n"
        f"    tags: {item['tags']}\n"
        f"    likes: {item.get('likes', 0)}\n"
        f"    created_at: {
            datetime.fromisoformat(
                str(
                    item.get('created_at')
                    )
                ).strftime(
                    '%Y-%m-%d %H:%M:%S'
                    )
                }\n"
        f"    url: {item['url']}\n"
    ]

    ai_block = format_ai_processed(item["ai_processed_data"])
    if ai_block:
        lines.append(ai_block)

    return "\n".join(lines) + "\n"


def output(data: list[ArticleData]) -> None:
    print("\n=======result========\n")

    for i, item in enumerate(data, 1):
        print(format_item(item, i))
