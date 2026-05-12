import requests
import json
import re
from datetime import date

# 兜底数据，确保即使爬不到也不会报错
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

# 1. 抓取 CNN 恐惧与贪婪指数
try:
    url = "https://money.cnn.com/data/fear-and-greed/"
    res = requests.get(url, timeout=8)
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
except Exception as e:
    print(f"获取恐惧贪婪指数失败: {e}")

# 2. 抓取 VIX 波动率指数
try:
    url = "https://finance.yahoo.com/quote/%5EVIX/"
    res = requests.get(url, timeout=8)
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
except Exception as e:
    print(f"获取VIX指数失败: {e}")

# 将最终数据写入 data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
