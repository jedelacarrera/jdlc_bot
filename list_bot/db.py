import psycopg2


class DbManager(object):	
		
	INSERT_LIST = "INSERT INTO lists (name, conversation) VALUES (%s, %s);"
	GET_LIST_BY_NAME = "SELECT * FROM lists WHERE name = %s and conversation = %s ORDER BY id DESC LIMIT 1;"
	GET_LAST_LIST = "SELECT * FROM lists WHERE conversation = %s ORDER BY id DESC LIMIT 1;"
	INSERT_PARTICIPANT = "INSERT INTO participants (list_id, phone, name, comment, going) VALUES (%s, %s, %s, %s, %s)"
	GET_PARTICIPANTS_BY_LIST_ID = "SELECT * FROM participants WHERE list_id = %s"
	GET_ALL_LISTS = "SELECT * FROM lists;"
	DELETE_PARTICIPANT = "DELETE FROM participants WHERE list_id = %s and phone = %s "

	def __init__(self, database_url):
		self.database_url = database_url
		self.connection = psycopg2.connect(database_url)
		self.cursor = self.connection.cursor()

	def insert_list(self, name, conversation):
		try:
			self.cursor.execute(DbManager.INSERT_LIST, (name, conversation))
		except Exception as e:
			print(e)

	def get_list_by_name(self, name, conversation):
		try: 
			self.cursor.execute(DbManager.GET_LIST_BY_NAME, (name, conversation))
			return self.cursor.fetchone()
		except Exception as e:
			print(e)
			return None

	def get_last_list(self, conversation):
		try: 
			self.cursor.execute(DbManager.GET_LAST_LIST, (conversation, ))
			return self.cursor.fetchone()
		except Exception as e: 
			print(e)
			return None

	def get_all_lists(self):
		try: 
			self.cursor.execute(DbManager.GET_ALL_LISTS)
			return self.cursor.fetchall()
		except Exception as e:
			print(e)
			return []

	def insert_participant(self, list_id, phone, name, comment, going):
		try: 
			self.cursor.execute(DbManager.DELETE_PARTICIPANT, (list_id, phone))
			return self.cursor.execute(DbManager.INSERT_PARTICIPANT, (list_id, phone, name, comment, going))
		except Exception as e:
			print(e)

	def get_participants_by_list_id(self, list_id):
		try: 
			self.cursor.execute(DbManager.GET_PARTICIPANTS_BY_LIST_ID, (list_id, ))
			return self.cursor.fetchall()
		except Exception as e:
			print(e)
			return []

	def commit(self):
		self.connection.commit()

if __name__ == "__main__":
	import os

	DATABASE_URL = os.environ['DATABASE_URL']
	db = DbManager(DATABASE_URL)

	# db.insert_list("A", "conversation1")  # 62
	# db.insert_list("B", "conversation1")  # 63
	# db.insert_list("A", "conversation2")  # 64
	# db.insert_list("C", "conversation2")  # 65
	# db.insert_list("D", "conversation2")  # 66
	# print(db.get_list_by_name("name1", "conversation1"))
	# print(db.get_last_list("conversation1"))
	print(db.get_all_lists())
	print(db.insert_participant(62, "5693231", "jorge", "yei!", True))
	print(db.get_participants_by_list_id(62))
	# db.commit()