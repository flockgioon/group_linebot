from random import choice
from linebot.models import TextSendMessage
from commands import command


@command("擲硬幣", "丟硬幣", "硬幣", "擲銅板", "丟銅板", "銅板", "coin")
def coin(rest: str) -> list:
    return [TextSendMessage(choice(["正", "反"]))]
