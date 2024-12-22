from typing import Optional, Tuple

import httpx
from tenacity import retry, stop_after_attempt, wait_random


@retry(wait=wait_random(min=3, max=5), stop=stop_after_attempt(5))
def get_bangumi_info(bangumi_url: str, chinese_name: Optional[str] = None) -> Tuple[str, str]:
    """
    Get bangumi info, first is summary, second is chinese name.

    :param bangumi_url: Bangumi URL
    :param chinese_name: Bangumi Chinese name. When it is None, it will auto fetch from bangumi.
    """
    summary = "!!!!!Fetch failed!!!!!"

    if bangumi_url[-1] == "/":
        bangumi_url = bangumi_url[:-1]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Host": "api.bgm.tv",
        "Connection": "keep-alive",
    }

    with httpx.Client(headers=headers, timeout=20) as client:
        response = client.get(bangumi_url)
        response.raise_for_status()

        res = response.json()

        summary = res["summary"]

        if chinese_name is None:
            try:
                chinese_name = res["name_cn"]
                if chinese_name is None or chinese_name == "":
                    raise ValueError("name_cn is empty")
            except Exception:
                chinese_name = res["name"]

            if chinese_name is None or chinese_name == "":
                chinese_name = "!!!!!Fetch Chinese Name failed!!!!!"

    return summary, chinese_name
