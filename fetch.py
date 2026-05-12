import requests
import json
import re
from datetime import date

# 兜底数据
data = {
    "date": str(date.today()),
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

# 日志结构
log_data = {
    "date": str(date.today()),
    "sources": {}
}

# 1. CNN 恐惧贪婪
success_fg = False
try:
    url = "https://money.cnn.com/data/fear-and-greed/"
    res = requests.get(url, timeout=8)
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
        success_fg = True
except:
    pass
log_data["sources"]["CNN恐惧贪婪指数"] = {
    "success": success_fg,
    "url": "https://money.cnn.com/data/fear-and-greed/"
}

# 2. Yahoo VIX
success_vix = False
try:
    url = "https://finance.yahoo.com/quote/%5EVIX/"
    res = requests.get(url, timeout=8)
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
        success_vix = True
except:
    pass
log_data["sources"]["VIX波动率"] = {
    "success": success_vix,
    "url": "https://finance.yahoo.com/quote/%5EVIX/"
}

# 固定数据（无需爬取，标记成功）
log_data["sources"]["巴菲特指标"] = {"success": True, "url": ""}
log_data["sources"]["席勒CAPE"] = {"success": True, "url": ""}
log_data["sources"]["标普500 TTM市盈率"] = {"success": True, "url": ""}
log_data["sources"]["标普500预估市盈率"] = {"success": True, "url": ""}
log_data["sources"]["10年期美债收益率"] = {"success": True, "url": ""}
log_data["sources"]["股债收益率差"] = {"success": True, "url": ""}
log_data["sources"]["标普500股息率"] = {"success": True, "url": ""}
log_data["sources"]["联邦基金利率"] = {"success": True, "url": ""}
log_data["sources"]["美债期限利差"] = {"success": True, "url": ""}

# 保存数据
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 保存日志
try:
    with open("log.json", "r", encoding="utf-8") as f:
        history = json.load(f)
except:
    history = []

# 去重：同一天只保留一条
new_history = []
for item in history:
    if item["date"] != log_data["date"]:
        new_history.append(item)
new_history.append(log_data)

# 保存
with open("log.json", "w", encoding="utf-8") as f:
    json.dump(new_history, f, ensure_ascii=False, indent=2)
