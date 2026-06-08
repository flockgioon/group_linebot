import asyncio
import json
import re
from typing import Tuple

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from linebot.models import TextSendMessage

from commands import command
import config

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
}

with open(config.DATA_DIR / "stocks_name_to_id.json", encoding="utf-8") as f:
    _name_to_id: dict[str, str] = json.load(f)

with open(config.DATA_DIR / "stocks_id_to_suffix.json", encoding="utf-8") as f:
    _id_to_suffix: dict[str, str] = json.load(f)


def _resolve_stock(keyword: str) -> Tuple[str | None, str | None]:
    stock_id = keyword
    if not keyword.isascii() or not keyword.isalnum():
        if keyword in _name_to_id:
            stock_id = _name_to_id[keyword]
        else:
            return keyword, None
    suffix = _id_to_suffix.get(stock_id)
    return stock_id, suffix


async def _fetch_all(urls: list[str]) -> list[str]:
    async with ClientSession() as session:
        tasks = [_fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)


async def _fetch_one(session: ClientSession, url: str) -> str:
    async with session.get(url, headers=_HEADERS) as resp:
        return await resp.text()


def _parse_stock_price(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    stock_name = soup.select_one(r".C\(\$c-link-text\)").text
    stock_sub = soup.select_one(r".C\(\$c-icon\)").text
    index_el = soup.select_one(r".Fz\(32px\)")
    net = soup.select_one(r".Fz\(20px\)").text
    pct = soup.select_one(r".Jc\(fe\)").text

    price = index_el.text
    classes = index_el.get("class", [])
    if "C($c-trend-up)" in classes:
        arrow = "▲"
    elif "C($c-trend-down)" in classes:
        arrow = "▼"
    else:
        arrow = "―"
    return f"{stock_name}({stock_sub}) : {price} ‖ {arrow} {net}{pct}"


@command("台股")
def stock(rest: str) -> list:
    include_index = not rest.strip() or any(kw in rest for kw in ("大盤", "加權指數"))
    cleaned = rest.replace("大盤", "").replace("加權指數", "")

    valid, invalid = [], []
    seen = set()
    for token in re.split(r"[ \n]+", cleaned):
        if not token:
            continue
        stock_id, suffix = _resolve_stock(token)
        if stock_id in seen:
            continue
        seen.add(stock_id)
        if suffix is not None:
            valid.append((stock_id, suffix))
        else:
            invalid.append(stock_id)

    if include_index:
        valid.insert(0, ("%5ETWII", ""))

    messages = []

    if valid:
        base = "https://tw.stock.yahoo.com/quote/"
        urls = [f"{base}{sid}{sfx}" for sid, sfx in valid]
        htmls = asyncio.run(_fetch_all(urls))
        lines = [_parse_stock_price(h) for h in htmls]
        messages.append(TextSendMessage("\n".join(lines)))

    if invalid:
        messages.append(TextSendMessage("未能找到以下股票 : \n\t\t\t\t" + ", ".join(invalid)))

    if not messages:
        messages.append(TextSendMessage("無搜索結果"))

    return messages
