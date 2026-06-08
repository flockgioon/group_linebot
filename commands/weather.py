import requests
from linebot.models import TextSendMessage
from commands import command
import config


@command("天氣預報")
def weather(rest: str) -> list:
    city = rest.split(" ")[0] if rest.strip() else ""
    if not city:
        return [TextSendMessage("請輸入縣市名稱，例如：天氣預報 台北市")]

    url = (
        "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
        f"?Authorization={config.MOTC_API}"
    )
    data = requests.get(url).json()
    locations = data["records"]["location"]

    for loc in locations:
        name = loc["locationName"]
        if city not in (name, name.replace("臺", "台")):
            continue

        time_labels = ["未來 6 小時內：\n", "未來 6 ~ 18 小時：\n", "未來 18 ~ 30 小時：\n"]
        parts = [city + "\n"]
        for t in range(3):
            we = {
                el["elementName"]: el["time"][t]["parameter"]["parameterName"]
                for el in loc["weatherElement"]
            }
            parts.append(
                f"{time_labels[t]}"
                f"\t天氣：{we['Wx']}\n"
                f"\t最高溫度：{we['MaxT']}°C\n"
                f"\t最低溫度：{we['MinT']}°C\n"
                f"\t舒適度：{we['CI']}\n"
                f"\t降雨機率：{we['PoP']}%"
            )
        return [TextSendMessage("\n\n".join(parts))]

    return [TextSendMessage("查無此地")]
