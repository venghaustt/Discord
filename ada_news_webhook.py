import feedparser
import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

FEEDS = {
    "Cardano News": "https://cardano.org/news/",
    "Cardano Foundation": "https://cardanofoundation.org/blog",
    "CoinDesk Cardano": "https://www.coindesk.com/tag/cardano/",
    "CoinMarketCap ADA": "https://coinmarketcap.com/currencies/cardano/news/",
}

def send_to_discord(source, title, link):
    message = {
        "content": f"""
🟢 **ADA News Update**

**Source:** {source}
**Headline:** {title}
**Link:** {link}

#ADA #Cardano #CryptoNews
"""
    }

    requests.post(DISCORD_WEBHOOK_URL, json=message)

def main():
    for source, feed_url in FEEDS.items():
        feed = feedparser.parse(feed_url)

        if feed.entries:
            latest = feed.entries[0]
            title = latest.title
            link = latest.link
            send_to_discord(source, title, link)

if __name__ == "__main__":
    main()
