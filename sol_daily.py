import os
from datetime import datetime, timezone

import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CMC_API_KEY = os.getenv("CMC_API_KEY")

if not WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL secret is missing.")

if not CMC_API_KEY:
    raise RuntimeError("CMC_API_KEY secret is missing.")

if WEBHOOK_URL.endswith("/github"):
    WEBHOOK_URL = WEBHOOK_URL[:-7]
elif WEBHOOK_URL.endswith("/slack"):
    WEBHOOK_URL = WEBHOOK_URL[:-6]

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

params = {
    "symbol": "SOL",
    "convert": "USD",
}

response = requests.get(url, headers=headers, params=params, timeout=15)
response.raise_for_status()

data = response.json()["data"]["SOL"]
quote = data["quote"]["USD"]

name = data["name"]
symbol = data["symbol"]
rank = data["cmc_rank"]

price = quote["price"]
change_24h = quote["percent_change_24h"]
change_7d = quote["percent_change_7d"]
market_cap = quote["market_cap"]
volume_24h = quote["volume_24h"]

status = "🟢 Bullish" if change_24h >= 0 else "🔴 Bearish"

payload = {
   "content": "☀️ **SOL Daily Crypto Report**",
    "embeds": [
        {
            "title": f"{name} ({symbol})",
            "description": "Powered by CoinMarketCap data.",
            "color": 3447003,
            "fields": [
                {"name": "Current Price", "value": f"${price:,.4f}", "inline": True},
                {"name": "24H Change", "value": f"{change_24h:+.2f}%", "inline": True},
                {"name": "7D Change", "value": f"{change_7d:+.2f}%", "inline": True},
                {"name": "Market Rank", "value": f"#{rank}", "inline": True},
                {"name": "Market Cap", "value": f"${market_cap:,.0f}", "inline": False},
                {"name": "24H Volume", "value": f"${volume_24h:,.0f}", "inline": False},
                {"name": "Status", "value": status, "inline": False},
                {"name": "Note", "value": "Not financial advice. Build patiently.", "inline": False},
            ],
            "footer": {
                "text": "Updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            },
        }
    ],
    "allowed_mentions": {"parse": []},
}

discord = requests.post(WEBHOOK_URL, json=payload, timeout=15)

if discord.status_code >= 400:
    raise RuntimeError(f"Discord returned {discord.status_code}: {discord.text}")

print("ADA report sent successfully.")
