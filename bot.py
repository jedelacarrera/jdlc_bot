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
from fun_bot.main import FunBot
from list_bot.main import ListBot
from crypto_bot.main import CryptoBot


class Bot(telepot.aio.helper.ChatHandler):

	hi_re = re.compile(r"^(\/)*hi$", re.IGNORECASE)

	def __init__(self, *args, **kwargs):
		super(Bot, self).__init__(*args, **kwargs)
		self._answer = random.randint(0,99)
		self.fun_bot = FunBot()
		self.crypto_bot = CryptoBot()
		self.list_bot = ListBot()

	def hi(self, msg):
		return "Hello {}, what's up?".format(msg["from"]["first_name"] + " " + msg["from"]["last_name"])

	async def open(self, initial_msg, seed):
		# print(initial_msg)
		try:
			message = "Hi {},\nwatch the commands list to make an action".format(initial_msg["from"]["first_name"] + " " + initial_msg["from"]["last_name"])
		except:
			message = "Hi,\nwatch the commands list to make an action"
		await self.sender.sendMessage(message)
		await self.on_chat_message(initial_msg)

		return True  # prevent on_message() from being called on the initial message

	async def on_chat_message(self, msg):
		print(msg) 
		try:
			text = msg['text']
		except ValueError:
			await self.sender.sendMessage('Give me a string, please.')
			return

		# check the guess against the answer ...
		try:
			if Bot.btc_re.match(text) != None:
				response_text = self.btc()

			elif Bot.eth_re.match(text) != None:
				response_text = self.eth()

			elif Bot.dolar_re.match(text) != None:
				response_text = self.dolar()

			elif Bot.btc_bittrex_re.match(text) != None:
				response_text = self.btc_bittrex()

			elif Bot.eth_bittrex_re.match(text) != None:
				response_text = self.eth_bittrex()

			elif Bot.hi_re.match(text) != None:
				response_text = self.hi(msg)
				
			elif Bot.all_re.match(text) != None:
				response_text = self.dolar()
				
				response_text += '\n\n' + self.eth()
				response_text += '\n\n' + self.eth_bittrex()
				time.sleep(1)
				response_text += '\n\n' + self.btc()
				response_text += '\n\n' + self.btc_bittrex()
				


			else:
				response_text = self.other_response()
		except Exception as e:
			response_text = "There was an error, try again later\nError: {}".format(e)
			raise e

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
TIMEOUT = int(os.getenv("TIMEOUT", 100))
# print(TOKEN)
print(TIMEOUT)

if not TOKEN:
	print('not token')
	print(TIMEOUT)
	sys.exit(1)

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Bot, timeout=TIMEOUT),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()