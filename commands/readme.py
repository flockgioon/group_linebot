from linebot.models import TextSendMessage
from commands import command


@command("使用說明")
def readme(rest: str) -> list:
    text = (
        "ver 3.0.0\n"
        "功能與其用途：\n"
        "🟢擲骰子/丟骰子\n"
        "🟢擲硬幣/丟硬幣\n"
        "🟢天氣預報\n"
        "🟢台股(價格)\n"
        "🟢Mygo圖包\n"
        "🟢衛星雲圖"
    )
    return [TextSendMessage(text)]
