import sys
import os
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import random
from fun_bot.main import FunBot
from list_bot.main import ListBot
from crypto_bot.main import CryptoBot


class Bot(telepot.aio.helper.ChatHandler):

	def __init__(self, *args, **kwargs):
		super(Bot, self).__init__(*args, **kwargs)
		self._answer = random.randint(0,99)
		self.fun_bot = FunBot()
		self.crypto_bot = CryptoBot()
		self.list_bot = ListBot()

	async def open(self, initial_msg, seed):
		# try:
		# 	message = "Hi {},\nwatch the commands list to make an action".format(initial_msg["from"]["first_name"] + " " + initial_msg["from"]["last_name"])
		# except:
		# 	message = "Hi,\nwatch the commands list to make an action"
		# await self.sender.sendMessage(message)
		await self.on_chat_message(initial_msg)

		return True  # prevent on_message() from being called on the initial message

	async def on_chat_message(self, msg):
		print(msg) 
		try:
			text = msg['text']
		except ValueError:
			await self.sender.sendMessage('Give me a string, please.')
			return

		try:
			response = None

			crypto_response = self.crypto_bot.handle_message(msg)
			list_response = self.list_bot.handle_message(msg)

			response = crypto_response if crypto_response != None else response
			response = list_response if list_response != None else response

			if response == None:
				response = self.fun_bot.random()


		except Exception as e:
			response = "There was an error, try again later\nError: {}".format(e)
			raise e
		if response:
			await self.sender.sendMessage(response, parse_mode='Markdown')
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