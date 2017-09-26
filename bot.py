import sys
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import requests
import simplejson as json
import random

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
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)
		self._answer = random.randint(0,99)

	def btc(self):
		info = requests.get("https://www.surbtc.com/api/v2/markets/btc-clp/ticker.json")
		info = info.json()
		text = "btc compra: {}\nbtc venta: {}\nVariacion 24h: {}\nVariacion 7d: {}".format(
			info["ticker"]["max_bid"][0],
			info["ticker"]["min_ask"][0],
			info["ticker"]["price_variation_24h"],
			info["ticker"]["price_variation_7d"]
			)
		return text

	def eth(self):
		info = requests.get("https://www.surbtc.com/api/v2/markets/eth-clp/ticker.json")
		info = info.json()
		text = "eth compra: {}\neth venta: {}\nVariacion 24h: {}\nVariacion 7d: {}".format(
			info["ticker"]["max_bid"][0],
			info["ticker"]["min_ask"][0],
			info["ticker"]["price_variation_24h"],
			info["ticker"]["price_variation_7d"]
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
			if text in ['btc', 'Btc', 'BTC', '/btc']:
				response_text = self.btc()
			elif text in ['eth', 'Eth', 'ETH', '/eth']:
				response_text = self.eth()
			elif text in ['hi', 'Hi', 'HI', '/hi']:
				response_text = self.hi(msg)
			else:
				response_text = self.other_response()
		except:
			response_text = "There was an error, try again later"

		await self.sender.sendMessage(response_text)
		return


	async def on__idle(self, event):
		# print('on__idle')
		try:
			# await self.sender.sendMessage('See you later...')
			self.close()
		except Exception as e:
			print('Error closing {}'.format(e))
		# print('not error here')


TOKEN = "332206016:AAGW4YCE24LL-cUrXsBZ83BshyUK9ejpnOs"

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=1000),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()