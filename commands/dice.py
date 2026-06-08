from random import randint
from linebot.models import TextSendMessage
from commands import command


@command("擲骰子", "丟骰子", "骰子", "擲色子", "丟色子", "色子", "dice")
def dice(rest: str) -> list:
    return [TextSendMessage(str(randint(1, 6)))]
