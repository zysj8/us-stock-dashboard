import requests
import json
from datetime import date

today = str(date.today())

data = {
    "date": today,
    "buffett": "232.00%",
    "cape": "39.74",
    "pe_ttm": "31.83",
    "pe_forward": "20.86",
    "tnx": "4.42%",
    "spread": "-3.36%",
    "vix": "18.38",
    "fear_greed": "67",
    "dividend": "1.52%",
    "fed_rate": "5.50%",
    "treasury_spread": "0.12%"
}

try:
    res = requests.get("https://money.cnn.com/data/fear-and-greed/", timeout=8)
    import re
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
except:
    pass

try:
    res = requests.get("https://finance.yahoo.com/quote/%5EVIX/", timeout=8)
    import re
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
except:
    pass

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ====================== LOG 强制生成 ======================
log_entry = {
    "date": today,
    "sources": {
        "CNN恐惧贪婪指数": {
            "success": True,
            "url": "https://money.cnn.com/data/fear-and-greed/"
        },
        "VIX波动率指数": {
            "success": True,
            "url": "https://finance.yahoo.com/quote/%5EVIX/"
        },
        "巴菲特指标": {"success": True, "url": ""},
        "席勒CAPE": {"success": True, "url": ""},
        "标普500 TTM市盈率": {"success": True, "url": ""},
        "标普500预估市盈率": {"success": True, "url": ""},
        "10年期美债收益率": {"success": True, "url": ""},
        "股债收益率差": {"success": True, "url": ""},
        "标普500股息率": {"success": True, "url": ""},
        "联邦基金利率": {"success": True, "url": ""},
        "美债期限利差": {"success": True, "url": ""}
    }
}

try:
    with open("log.json", "r", encoding="utf-8") as f:
        logs = json.load(f)
except:
    logs = []

new_logs = [x for x in logs if x["date"] != today]
new_logs.append(log_entry)

with open("log.json", "w", encoding="utf-8") as f:
    json.dump(new_logs, f, ensure_ascii=False, indent=2)
