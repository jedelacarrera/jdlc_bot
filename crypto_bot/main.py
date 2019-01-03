"""Crypto Library."""
import requests
import time
import re


class CryptoBot(object):
    """Crypto class."""

    btc_re = re.compile(r"^(\/)*btc$", re.IGNORECASE)
    eth_re = re.compile(r"^(\/)*eth$", re.IGNORECASE)
    hi_re = re.compile(r"^(\/)*hi$", re.IGNORECASE)
    dolar_re = re.compile(r"^(\/)*dolar$", re.IGNORECASE)
    all_re = re.compile(r"^(\/)*all$", re.IGNORECASE)

    btc_bittrex_re = re.compile(r"^(\/)*btc_", re.IGNORECASE)
    eth_bittrex_re = re.compile(r"^(\/)*eth_", re.IGNORECASE)

    def handle_message(self, message):
        """Handle any message."""
        message = message["text"]
        response = None
        if self.btc_re.match(message) is not None:
            response = self.btc()

        elif self.eth_re.match(message) is not None:
            response = self.eth()

        elif self.dolar_re.match(message) is not None:
            response = self.dolar()

        elif self.btc_bittrex_re.match(message) is not None:
            response = self.btc_bittrex()

        elif self.eth_bittrex_re.match(message) is not None:
            response = self.eth_bittrex()

        elif self.all_re.match(message) is not None:
            response = self.all()

        return response

    def btc(self):
        """Request bitcoin data."""
        info = requests.get(
            "https://www.buda.com/api/v2/markets/btc-clp/ticker.json")
        info = info.json()
        text = "btc compra: ${:,.0f}\nbtc venta: ${:,.0f}\n" \
            + "Variacion 24h: {:,.1f}%\nVariacion 7d: {:,.1f}%"
        text = text.format(
            float(info["ticker"]["max_bid"][0]),
            float(info["ticker"]["min_ask"][0]),
            float(info["ticker"]["price_variation_24h"]) * 100,
            float(info["ticker"]["price_variation_7d"]) * 100
        )
        return text

    def eth(self):
        """Request ethereum data."""
        info = requests.get(
            "https://www.buda.com/api/v2/markets/eth-clp/ticker.json")
        info = info.json()
        text = "eth compra: ${:,.0f}\neth venta: ${:,.0f}\n" \
            + "Variacion 24h: {:,.1f}%\nVariacion 7d: {:,.1f}%"
        text = text.format(
            float(info["ticker"]["max_bid"][0]),
            float(info["ticker"]["min_ask"][0]),
            float(info["ticker"]["price_variation_24h"]) * 100,
            float(info["ticker"]["price_variation_7d"]) * 100
        )
        return text

    def dolar(self):
        """Request dolar data."""
        info = requests.get("http://mindicador.cl/api/")
        info = info.json()["dolar"]
        text = "Precio dolar {}: ${}".format(info["fecha"][:10], info["valor"])
        return text

    def btc_bittrex(self):
        """Request bitcoin data in bittrex."""
        info = requests.get(
            "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC")
        info = info.json()
        dolar = requests.get("http://mindicador.cl/api/").json()["dolar"]
        dolar = float(dolar["valor"])
        text = "btc compra: US${:,.0f} -> ${:,.0f}\n" \
            + "btc venta: US${:,.0f} -> ${:,.0f}"
        text = text.format(
            info["result"]["Bid"], info["result"]["Bid"] * dolar,
            info["result"]["Ask"], info["result"]["Ask"] * dolar,
        )
        return text

    def eth_bittrex(self):
        """Request ethereum data in bittrex."""
        info = requests.get(
            "https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH")
        info = info.json()
        dolar = requests.get("http://mindicador.cl/api/").json()["dolar"]
        dolar = float(dolar["valor"])
        text = "eth compra: US${:,.2f} -> ${:,.0f}\n" \
            + "eth venta: US${:,.2f} -> ${:,.0f}"
        text = text.format(
            info["result"]["Bid"], info["result"]["Bid"] * dolar,
            info["result"]["Ask"], info["result"]["Ask"] * dolar,
        )
        return text

    def all(self):
        """Request all info."""
        text = self.dolar()

        text += '\n\n' + self.eth()
        text += '\n\n' + self.eth_bittrex()
        time.sleep(1)
        text += '\n\n' + self.btc()
        text += '\n\n' + self.btc_bittrex()

        return text


if __name__ == "__main__":
    bot = CryptoBot()
    print(bot.handle_message({"text": "/btc"}))
    print(bot.handle_message({"text": "/all"}))
    print(bot.handle_message({"text": "/nada"}))
