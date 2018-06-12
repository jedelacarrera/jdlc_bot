import os
import psycopg2
import list_bot.db

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)

class ListBot(object):
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL)

	def __init__(self):
		pass




		