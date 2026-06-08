import json
import re
from random import randint
from urllib.parse import quote

from linebot.models import ImageSendMessage

from listeners import listener
import config

with open(config.DATA_DIR / "mygo_dict.json", encoding="utf-8") as f:
    _mygo_dict: dict[str, list] = json.load(f)

_punctuations = [' ', "'", '"', '(', ')', ',', '[', ']', '…', '！', '＂', '？', "?", "!", "...", "（", "）"]
_strip_re = re.compile("|".join(re.escape(p) for p in _punctuations))

_stripped_to_key: dict[str, str] = {}
for key in _mygo_dict:
    _stripped_to_key[_strip_re.sub("", key)] = key


@listener
def mygo(text: str) -> list:
    normalized = _strip_re.sub("", text)
    if normalized in _stripped_to_key:
        text = _stripped_to_key[normalized]

    if text not in _mygo_dict:
        return []

    entry = _mygo_dict[text]
    count, filenames = entry[0], entry[1:]
    chosen = filenames[randint(0, count - 1)]
    url = config.MYGO_BASE_URL + quote(chosen)
    return [ImageSendMessage(original_content_url=url, preview_image_url=url)]
