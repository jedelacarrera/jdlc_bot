import os
import psycopg2
from list_bot.db import DbManager
import re

DATABASE_URL = os.environ['DATABASE_URL']

class ListBot(object):
	DATABASE_URL = os.environ['DATABASE_URL']
	list_re = re.compile(r"^((\/)|(!))*list", re.IGNORECASE)
	new_re = re.compile(r"^((\/)|(!))*new", re.IGNORECASE)
	yes_re = re.compile(r"^((\/)|(!))*yes", re.IGNORECASE)
	no_re = re.compile(r"^((\/)|(!))*no", re.IGNORECASE)


	def __init__(self):
		self.db = DbManager(self.DATABASE_URL)

	def handle_message(self, message):
		message["text"] = message["text"].lower()
		text = message["text"]
		if self.list_re.match(text) != None:
			return self.list_information(message)

		if self.new_re.match(text) != None:
			return self.new(message)

		if self.yes_re.match(text) != None:
			return self.yes(message)

		if self.no_re.match(text) != None:
			return self.no(message)

	def get_list(self, message):
		splitted_text = message["text"].split()[1:]
		name = splitted_text[0] if len(splitted_text) > 0 else None
		conversation = str(message["chat"]["id"])
		print(name, conversation)
		list_instance = None
		if name:
			list_instance = self.db.get_list_by_name(name, conversation)
		if not list_instance:
			list_instance = self.db.get_last_list(conversation)
		return list_instance

	def list_information(self, message):
		list_instance = self.get_list(message)
		if not list_instance:
			return "No hay ninguna lista, crea una con el comando 'new'"
		participants = self.db.get_participants_by_list_id(list_instance[0])
		text = "*Lista {}*\n*Van:*\n{}*No van:*\n{}"
		going = []
		not_going = []
		for participant in participants:
			if participant[5]:
				going.append("{}. {} - {}\n".format(len(going) + 1, participant[3], participant[4]))
			else:
				not_going.append("{}. {} - {}\n".format(len(not_going) + 1, participant[3], participant[4]))

		return text.format(list_instance[1], "".join(going), "".join(not_going))

	def new(self, message):
		splitted_text = message["text"].split()[1:]
		name = splitted_text[0] if len(splitted_text) > 0 else ""
		conversation = str(message["chat"]["id"])
		self.db.insert_list(name, conversation)
		self.db.commit()
		return "lista creada"

	def yes(self, message):
		return self.insert_participant(message, True)

	def no(self, message):
		return self.insert_participant(message, False)

	def insert_participant(self, message, going=True):
		list_instance = self.get_list(message)
		if not list_instance:
			return "list not found"
		list_id = list_instance[0]
		splitted_text = message["text"].split()[1:]
		if len(splitted_text) > 0 and splitted_text[0] == list_instance[1]:
			splitted_text = splitted_text[1:]
		comment = " ".join(splitted_text)

		name = message['from']['first_name'] + ' ' + message['from']['last_name']
		self.db.insert_participant(list_id, str(message['from']['id']), name, comment, going)
		self.db.commit()
		return False
		