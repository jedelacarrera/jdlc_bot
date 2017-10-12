import sys
import os
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import requests
import simplejson as json
import random
import re

FUN_FACTS = [
	"McDonalds calls frequent buyers of their food heavy users.",
	"The average person spends 6 months of their lifetime waiting on a red light to turn green.",
	"The largest recorded snowflake was in Keogh, MT during year 1887, and was 15 inches wide.",
	"You burn more calories sleeping than you do watching television.",
	"There are more lifeforms living on your skin than there are people on the planet.",
	"Southern sea otters have flaps of skin under their forelegs that act as pockets. When diving, they use these pouches to store rocks and food.",
	"In 1386 a pig in France was executed by public hanging for the murder of a child.",
	"One in every five adults believe that aliens are hiding in our planet disguised as humans.",
	"If you believe that you’re truly one in a million, there are still approximately 7,184 more people out there just like you.",
	"A single cloud can weight more than 1 million pounds.",
	"A human will eat on average 70 assorted insects and 10 spiders while sleeping.",
	"James Buchanan, the 15th U.S. president continuously bought slaves with his own money in order to free them.",
	"There are more possible iterations of a game of chess than there are atoms in the known universe.",
	"The average person walks the equivalent of three times around the world in a lifetime.",
	"Men are 6 times more likely to be struck by lightning than women.",
	"Coca-Cola would be green if coloring wasn’t added to it.",
	"You cannot snore and dream at the same time."
]


class Player(telepot.aio.helper.ChatHandler):
	btc_re = re.compile(r"^(\/)*btc$", re.IGNORECASE)
	eth_re = re.compile(r"^(\/)*eth$", re.IGNORECASE)
	hi_re = re.compile(r"^(\/)*hi$", re.IGNORECASE)
	dolar_re = re.compile(r"^(\/)*dolar$", re.IGNORECASE)
	all_re = re.compile(r"^(\/)*all$", re.IGNORECASE)

	btc_bittrex_re = re.compile(r"^(\/)*btc_", re.IGNORECASE)
	eth_bittrex_re = re.compile(r"^(\/)*eth_", re.IGNORECASE)


	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)
		self._answer = random.randint(0,99)

	def btc(self):
		info = requests.get("https://www.surbtc.com/api/v2/markets/btc-clp/ticker.json")
		info = info.json()
		text = "btc compra: ${}\nbtc venta: ${}\nVariacion 24h: {}\nVariacion 7d: {}".format(
			info["ticker"]["max_bid"][0],
			info["ticker"]["min_ask"][0],
			info["ticker"]["price_variation_24h"],
			info["ticker"]["price_variation_7d"]
			)
		return text

	def eth(self):
		info = requests.get("https://www.surbtc.com/api/v2/markets/eth-clp/ticker.json")
		info = info.json()
		text = "eth compra: ${}\neth venta: ${}\nVariacion 24h: {}\nVariacion 7d: {}".format(
			info["ticker"]["max_bid"][0],
			info["ticker"]["min_ask"][0],
			info["ticker"]["price_variation_24h"],
			info["ticker"]["price_variation_7d"]
			)
		return text

	def dolar(self):
		info = requests.get("http://mindicador.cl/api/")
		info = info.json()["dolar"]
		text = "Precio dolar {}: ${}".format(info["fecha"][:10], info["valor"])
		return text

	def btc_bittrex(self):
		info = requests.get("https://bittrex.com/api/v1.1/public/getticker", data={"market": "USDT-BTC"}).json()
		dolar = float(requests.get("http://mindicador.cl/api/").json()["dolar"]["valor"])
		text = "btc compra: US${:,.0f} -> ${:,.0f}\nbtc venta: US${:,.0f} -> ${:,.0f}".format(
			info["result"]["Bid"], info["result"]["Bid"] * dolar,
			info["result"]["Ask"], info["result"]["Ask"] * dolar,
			)
		return text

	def eth_bittrex(self):
		info = requests.get("https://bittrex.com/api/v1.1/public/getticker", data={"market": "USDT-ETH"}).json()
		dolar = float(requests.get("http://mindicador.cl/api/").json()["dolar"]["valor"])
		text = "eth compra: US${:,.2f} -> ${:,.0f}\neth venta: US${:,.2f} -> ${:,.0f}".format(
			info["result"]["Bid"], info["result"]["Bid"] * dolar,
			info["result"]["Ask"], info["result"]["Ask"] * dolar,
			)
		return text

	def hi(self, msg):
		return "Hello {}, what's up?".format(msg["from"]["first_name"] + " " + msg["from"]["last_name"])

	def other_response(self):
		return "Did you know?\n" + random.choice(FUN_FACTS)

	async def open(self, initial_msg, seed):
		# print(initial_msg)
		try:
			message = """Hi {}, send me one of these:
			btc (for bitcoin value in surbtc)
			eth (for ethereum value in surbtc)
			hi (for a greeting message)""".format(initial_msg["from"]["first_name"] + " " + initial_msg["from"]["last_name"])
		except:
			message = """Hi, send me one of these:
			btc (for bitcoin value in surbtc)
			eth (for ethereum value in surbtc)
			hi (for a greeting message)"""
		await self.sender.sendMessage(message)
			
		return True  # prevent on_message() from being called on the initial message

	async def on_chat_message(self, msg):
		# print(msg)
		try:
			text = msg['text']
		except ValueError:
			await self.sender.sendMessage('Give me a string, please.')
			return

		# check the guess against the answer ...
		try:
			if Player.btc_re.match(text) != None:
				response_text = self.btc()

			elif Player.eth_re.match(text) != None:
				response_text = self.eth()

			elif Player.dolar_re.match(text) != None:
				response_text = self.dolar()

			elif Player.btc_bittrex_re.match(text) != None:
				response_text = self.btc_bittrex()

			elif Player.eth_bittrex_re.match(text) != None:
				response_text = self.eth_bittrex()

			elif Player.hi_re.match(text) != None:
				response_text = self.hi(msg)
			elif Player.all_re.match(text) != None:
				response_text = self.dolar()
				response_text += '\n\n' + self.btc()
				response_text += '\n\n' + self.btc_bittrex()
				response_text += '\n\n' + self.eth()
				response_text += '\n\n' + self.eth_bittrex()

			else:
				response_text = self.other_response()
		except Exception as e:
			response_text = "There was an error, try again later\nError: {}".format(e)

		await self.sender.sendMessage(response_text)
		return


	# async def on__idle(self, event):
	# 	# print('on__idle')
	# 	# await self.sender.sendMessage('See you later...')
	# 	self.close()
	# 	# print('not error here')

	async def on_close(self, e):
		print(e)
		# self.close()


TOKEN = os.getenv("TOKEN", "479455539:AAERXML5_y6sAZp_2EpziB7mUSNYONNiduo")
TIMEOUT = int(os.getenv("TIMEOUT", 10))
# print(TOKEN)
print(TIMEOUT)

if not TOKEN:
	print('not token')
	print(TIMEOUT)
	sys.exit(1)

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=TIMEOUT),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()