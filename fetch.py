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
    "dividend": "1.52%",      # 标普500股息率
    "fed_rate": "5.50%",      # 美联储利率
    "treasury_spread": "0.12%"# 美债利差
}

# 1. 恐惧贪婪
try:
    url = "https://money.cnn.com/data/fear-and-greed/"
    res = requests.get(url, timeout=8)
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
except:
    pass

# 2. VIX
try:
    url = "https://finance.yahoo.com/quote/%5EVIX/"
    res = requests.get(url, timeout=8)
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
except:
    pass

# 写入最终数据
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
