import requests
import json
from datetime import date

# 兜底默认数据
data = {
    "date": str(date.today()),
    "buffett": "232.00%",
    "cape": "39.74",
    "pe_ttm": "31.83",
    "pe_forward": "20.86",
    "tnx": "4.42%",
    "spread": "-3.36%",
    "vix": "18.38",
    "fear_greed": "67"
}

# 抓取 CNN 恐惧贪婪指数
try:
    url = "https://money.cnn.com/data/fear-and-greed/"
    res = requests.get(url, timeout=10)
    import re
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
except Exception:
    pass

# 抓取 VIX 波动率
try:
    url = "https://finance.yahoo.com/quote/%5EVIX/"
    res = requests.get(url, timeout=10)
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
except Exception:
    pass

# 保存到 data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
