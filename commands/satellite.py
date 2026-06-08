import pytz
from datetime import datetime
from linebot.models import ImageSendMessage

from commands import command
import config


@command("衛星雲圖")
def satellite(rest: str) -> list:
    tz = pytz.timezone(config.TIMEZONE)
    now = datetime.now(tz)
    ts = now.strftime("?%Y-%m-%dT%H:%M:%S%z")
    ts = ts[:-2] + ":" + ts[-2:]
    url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-B0032-002.jpg" + ts
    return [ImageSendMessage(original_content_url=url, preview_image_url=url)]
