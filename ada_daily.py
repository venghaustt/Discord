import os
from datetime import datetime, timezone

import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL secret is missing.")

# If the webhook URL accidentally ends with /github or /slack,
# convert it back to a standard Discord webhook.
if WEBHOOK_URL.endswith("/github"):
    WEBHOOK_URL = WEBHOOK_URL[:-7]
elif WEBHOOK_URL.endswith("/slack"):
    WEBHOOK_URL = WEBHOOK_URL[:-6]

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "cardano",
    "vs_currencies": "usd",
    "include_24hr_change": "true",
    "include_market_cap": "true",
    "include_24hr_vol": "true"
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()["cardano"]

price = data["usd"]
change = data["usd_24h_change"]
market_cap = data["usd_market_cap"]
volume = data["usd_24h_vol"]

status = "🟢 Bullish" if change >= 0 else "🔴 Bearish"

payload = {
    "content": "💠 **ADA Daily Crypto Report**",
    "embeds": [
        {
            "title": "Cardano (ADA)",
            "color": 3447003,
            "fields": [
                {
                    "name": "Current Price",
                    "value": f"${price:,.4f}",
                    "inline": True
                },
                {
                    "name": "24H Change",
                    "value": f"{change:+.2f}%",
                    "inline": True
                },
                {
                    "name": "Status",
                    "value": status,
                    "inline": True
                },
                {
                    "name": "Market Cap",
                    "value": f"${market_cap:,.0f}",
                    "inline": False
                },
                {
                    "name": "24H Volume",
                    "value": f"${volume:,.0f}",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            }
        }
    ]
}

discord = requests.post(WEBHOOK_URL, json=payload, timeout=15)

if discord.status_code >= 400:
    raise RuntimeError(
        f"Discord returned {discord.status_code}: {discord.text}"
    )

print("ADA report sent successfully.")
