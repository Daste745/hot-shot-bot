import requests
from os import getenv
from time import sleep

import dotenv
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed


dotenv.load_dotenv()


def get_soup(url: str) -> BeautifulSoup:
    request = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
        },
    )

    return BeautifulSoup(
        request.content,
        features="html.parser",
    )


def main():
    webhook = DiscordWebhook(url=getenv("WEBHOOK_URL"))

    while True:
        soup = get_soup("https://www.x-kom.pl/goracy_strzal")
        sleep(4)

        item_name = soup.select("h1.sc-1bker4h-4")[0].string
        item_id = soup.select("span.sc-1bker4h-9")[0].contents[-1]
        image_url = soup.select("span.hEGONW")[0].contents[0]["src"]
        image_url = image_url.replace("product-mini", "product-new-big")
        old_price = soup.select("span.sc-8c7p9j-3")[0].string
        new_price = soup.select("span.sc-8c7p9j-2")[0].string
        product_url = f"https://www.x-kom.pl/p/{item_id}"

        print(
            f"Got Hot Shot, product name: {item_name} id: {item_id} "
            f"permalink: {product_url}"
        )

        embed = DiscordEmbed(
            title="Hot Shot",
            description=f"[{item_name}]({product_url})",
            url="https://www.x-kom.pl/goracy_strzal",
            color=242424,
        )
        embed.set_thumbnail(url=image_url)
        embed.add_embed_field(
            name="Price",
            value=f"~~**{old_price}**~~ ➡️ **{new_price}**",
            inline=False,
        )
        embed.set_timestamp()
        webhook.add_embed(embed)

        webhook_response = webhook.execute()
        print(f"Sent webhook: {webhook_response}")
        webhook.embeds.clear()

        hours, minutes, _ = map(lambda x: int(x.string), soup.select("div.ntliq5-4"))
        print(f"Waiting {hours}h {minutes + 1}m for next Hot Shot")
        sleep(hours * 3600 + minutes * 60 + 62)


if __name__ == "__main__":
    main()
