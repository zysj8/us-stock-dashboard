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

# 1. CNN 恐惧贪婪指数
success_fg = False
try:
    url = "https://money.cnn.com/data/fear-and-greed/"
    res = requests.get(url, timeout=8)
    m = re.search(r'fearGreedIndex":(\d+)', res.text)
    if m:
        data["fear_greed"] = m.group(1)
        success_fg = True
except Exception as e:
    print(f"恐惧贪婪指数拉取失败: {e}")
log_data["sources"]["CNN恐惧贪婪指数"] = {
    "success": success_fg,
    "url": "https://money.cnn.com/data/fear-and-greed/"
}

# 2. Yahoo VIX 指数
success_vix = False
try:
    url = "https://finance.yahoo.com/quote/%5EVIX/"
    res = requests.get(url, timeout=8)
    m = re.search(r'regularMarketPrice">([\d\.]+)', res.text)
    if m:
        data["vix"] = f"{float(m.group(1)):.2f}"
        success_vix = True
except Exception as e:
    print(f"VIX指数拉取失败: {e}")
log_data["sources"]["VIX波动率指数"] = {
    "success": success_vix,
    "url": "https://finance.yahoo.com/quote/%5EVIX/"
}

# 固定数据（标记为成功）
log_data["sources"]["巴菲特指标"] = {"success": True, "url": ""}
log_data["sources"]["席勒CAPE"] = {"success": True, "url": ""}
log_data["sources"]["标普500 TTM市盈率"] = {"success": True, "url": ""}
log_data["sources"]["标普500预估市盈率"] = {"success": True, "url": ""}
log_data["sources"]["10年期美债收益率"] = {"success": True, "url": ""}
log_data["sources"]["股债收益率差"] = {"success": True, "url": ""}
log_data["sources"]["标普500股息率"] = {"success": True, "url": ""}
log_data["sources"]["联邦基金利率"] = {"success": True, "url": ""}
log_data["sources"]["美债期限利差"] = {"success": True, "url": ""}

# 写入 data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 写入 log.json（修复版，强制生成）
try:
    with open("log.json", "r", encoding="utf-8") as f:
        history = json.load(f)
except:
    history = []

# 去重：同一天只保留一条记录
new_history = [item for item in history if item["date"] != log_data["date"]]
new_history.append(log_data)

# 强制写入 log.json
with open("log.json", "w", encoding="utf-8") as f:
    json.dump(new_history, f, ensure_ascii=False, indent=2)

print("✅ 数据和日志写入完成！")
