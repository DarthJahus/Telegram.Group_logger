#----------------------------------------------#
# LogTBot | Jahus | 2015-09-03                 #
#----------------------------------------------#----------------
# Forked from Dj4x 3.21.20
# Change log
# * 2015-09-03 :
#     (1.0.0)               - First code
# * 2015-09-04 :
#     (1.0.1)               - Showing sender.id in bot log.
# * 2015-09-06 :
#     (1.1.1)               - Sending log via Telegram
#                             Command /get_log
#     (1.2.1)               - Handling photo messages
#     (1.2.2)               - Minor bug fix
#---------------------------------------------------------------
# IMPORTS
#---------------------------------------------------------------
import json
import requests
import time
#---------------------------------------------------------------
# DATA
#---------------------------------------------------------------
def load_file_json(file_name):
	with open(file_name, 'r') as _file:
		content = _file.read()
		content_dict = json.loads(content)
		return content_dict
# CONFIG FILES
data_file = {
	"config": "logger_config.json"
}
config = load_file_json(data_file.get("config"))
# VARIABLES
HALT = False
PAUSE = {"xsomechannelx": True}
__name__ = config.get("bot_name")
__version__ = config.get("bot_version")
print("#---------------------------------------------------------------")
print("# %s version %s, by Jahus." % (__name__, __version__))
print("#---------------------------------------------------------------")
#---------------------------------------------------------------
# Telegram :: Classes
#---------------------------------------------------------------
#
# This object represents a Telegram user or bot.
class telegram_classes_User:
	def __init__(self, data_json):
		# id: Integer -- Unique identifier for this user or bot
		self.id = data_json.get("id")
		# first_name: String -- User's or bot's first name
		self.first_name = data_json.get("first_name")
		# last_name: String -- (Optional) User's or bot's last name
		if "last_name" in data_json:
			self.last_name = data_json.get("last_name")
		else:
			self.last_name = -1
		# user_name: String -- (Optional) User's or bot's username (without @)
		if "username" in data_json:
			self.username = data_json.get("username")
		else:
			self.username = -1
	def __str__(self):
		r_str = "User #%s | First name: %s" % (self.id, self.first_name)
		if self.last_name != -1:
			r_str += " | Last name: %s" % (self.last_name)
		if self.username != -1:
			r_str += " | Username: @%s" % (self.username)
		return r_str
#
# This object represents a group chat.
class telegram_classes_GroupChat:
	def __init__(self, data_json):
		self.id = data_json.get("id")
		self.title = data_json.get("title")
	def __str__(self):
		return "Group chat #%s: ""%s""" % (self.id, self.title)
# Types for Message
telegram_types = {
	"text": "T",
	"forward_from": "F",
	"reply_to_message": "R",
	"audio": "A",
	"document": "G",
	"photo": "I",
	"sticker": "S",
	"video": "V",
	"contact": "U",
	"location": "L",
	"new_chat_participant": "cpn",
	"left_chat_participant": "cpl",
	"new_chat_title": "ctn",
	"new_chat_photo": "cin",
	"delete_chat_photo": "cid",
	"group_chat_created": "gcc"
}
#
class telegram_classes_Message:
	def __init__(self, data_json):
		self.type = ""
		self.message_id = data_json.get("message_id")
		self.sender = telegram_classes_User(data_json.get("from"))
		self.date = data_json.get("date")
		if "title" in data_json.get("chat"):
			# GroupChat
			self.chat = telegram_classes_GroupChat(data_json.get("chat"))
		else:
			# PrivateChat (User)
			self.chat = telegram_classes_User(data_json.get("chat"))
		if "forward_from" in data_json:
			self.forward_from = telegram_classes_User(data_json.get("forward_from"))
			if telegram_types.get("forward_from") not in self.type: self.type += telegram_types.get("forward_from")
		if "forward_date" in data_json:
			self.forward_date = data_json.get("forward_date")
		if "reply_to_message" in data_json:
			self.reply_to_message = telegram_classes_Message(data_json.get("reply_to_message"))
			if telegram_types.get("reply_to_message") not in self.type: self.type += telegram_types.get("reply_to_message")
		if "text" in data_json:
			self.text = data_json.get("text")
			if telegram_types.get("text") not in self.type: self.type += telegram_types.get("text")
		if "audio" in data_json:
			self.audio = data_json.get("audio") #TODO: Audio structure
			if telegram_types.get("audio") not in self.type: self.type += telegram_types.get("audio")
		if "document" in data_json:
			self.document = data_json.get("document") #TODO: Document structure
			if telegram_types.get("document") not in self.type: self.type += telegram_types.get("document")
		if "photo" in data_json:
			self.photo = data_json.get("photo") #TODO: Photo structure
			if telegram_types.get("photo") not in self.type: self.type += telegram_types.get("photo")
		if "sticker" in data_json:
			self.sticker = data_json.get("sticker") #TODO: Sticker structure
			if telegram_types.get("sticker") not in self.type: self.type += telegram_types.get("sticker")
		if "video" in data_json:
			self.video = data_json.get("video") #TODO: Video structure
			if telegram_types.get("video") not in self.type: self.type += telegram_types.get("video")
		if "caption" in data_json:
			self.caption = data_json.get("caption")
		if "contact" in data_json:
			self.contact = data_json.get("contact") #TODO: Contact structure
			if telegram_types.get("contact") not in self.type: self.type += telegram_types.get("contact")
		if "location" in data_json:
			self.location = data_json.get("location") #TODO: Location structure
			if telegram_types.get("location") not in self.type: self.type += telegram_types.get("location")
		if "new_chat_participant" in data_json:
			self.new_chat_participant = telegram_classes_User(data_json.get("new_chat_participant"))
			if telegram_types.get("new_chat_participant") not in self.type: self.type += telegram_types.get("new_chat_participant")
		if "left_chat_participant" in data_json:
			self.left_chat_participant = telegram_classes_User(data_json.get("left_chat_participant"))
			if telegram_types.get("left_chat_participant") not in self.type: self.type += telegram_types.get("left_chat_participant")
		if "new_chat_title" in data_json:
			self.new_chat_title = data_json.get("new_chat_title")
			if telegram_types.get("new_chat_title") not in self.type: self.type += telegram_types.get("new_chat_title")
		if "new_chat_photo" in data_json:
			self.new_chat_photo = data_json.get("new_chat_photo") #TODO: Photo structure
			if telegram_types.get("new_chat_photo") not in self.type: self.type += telegram_types.get("new_chat_photo")
		if "delete_chat_photo" in data_json:
			self.delete_chat_photo = data_json.get("delete_chat_photo") # Boolean
			if telegram_types.get("delete_chat_photo") not in self.type: self.type += telegram_types.get("delete_chat_photo")
		if "group_chat_created" in data_json:
			self.group_chat_created = data_json.get("group_chat_created") # Boolean
			if telegram_types.get("group_chat_created") not in self.type: self.type += telegram_types.get("group_chat_created")
	def __str__(self):
		return "Message #%s at %s. From %s to %s." % (self.message_id, self.date, self.sender, self.chat)
#
class telegram_classes_Document:
	def __init__(self, data_json):
		self.file_id = data_json.get("file_id")
		if "thumb" in data_json:
			self.thumb = data_json.get("thumb")
		else:
			self.thumb = None
		if "file_name" in data_json:
			self.file_name = data_json.get("file_name")
		else:
			self.file_name = None
		if "mime_type" in data_json:
			self.mime_type = data_json.get("mime_type")
		else:
			self.mime_type = None
		if "file_size" in data_json:
			self.file_size = data_json.get("file_size")
		else:
			self.file_size = None			
#
class telegram_classes_PhotoSize:
	def __init__(self, data_json):
		self.file_id = data_json.get("file_id")
		self.width = data_json.get("width")
		self.height = data_json.get("height")
		if "file_size" in data_json:
			self.file_size = data_json.get("file_size")
#
class telegram_classes_Update:
	def __init__(self, data_json):
		self.message = telegram_classes_Message(data_json.get("message"))
		self.update_id = data_json.get("update_id")
	def __str__(self):
		return "Update #%s | %s" % (self.update_id, self.message)
#
#---------------------------------------------------------------
# Telegram :: Bot
#---------------------------------------------------------------
telegram_bot_token = config.get("telegram_params").get("token")
telegram_bot_request = "https://api.telegram.org/bot"
telegram_groups = config.get("groups")
# send_to_IRC = True
# telegram_bifrost_enabled = False
#
telegram_bot_info = None
telegram_bot_offset = 0
#
def telegram_bot_get_bot_info():
	#+DEBUG
	print("** telegram_bot_get_bot_info(): getting bot information...")
	#/DEBUG
	global telegram_bot_info
	req = requests.get("%s%s%s" % (telegram_bot_request, telegram_bot_token, "/getMe"))
	if (req.status_code != 200):
		print("Error %s" % req.status_code)
	else:
		req_json = req.json()
		if "ok" in req_json:
			if (req_json.get("ok") == True):
				_me = telegram_classes_User(req_json.get("result"))
				telegram_bot_info = _me
				print(telegram_bot_info)
			else:
				print("Error %s" % "There has been an unknown error")
		else:
			print("Error %s" & "There has been an unknown error.")
#
def telegram_bot_get_updates():
	global telegram_bot_offset
	# Options
	# 	offset: integer -- (Optional)
	# 	limit: integer -- (Optional)
	#   timeout: integer -- (Optional)
	req_data = {"offset": telegram_bot_offset + 1, "limit": "", "timeout": ""}
	req = requests.get("%s%s%s" % (telegram_bot_request, telegram_bot_token, "/getUpdates"), data = req_data)
	if (req.status_code != 200):
		print("Error %s" % req.status_code)
	else:
		req_json = req.json()
		# print(req_json)
		if "ok" in req_json:
			if (req_json.get("ok") == True):
				# print("-- telegram_bot_get_updates(): Got %s updates." % len(req_json.get("result")))
				for update_json in req_json.get("result"):
					_update = telegram_classes_Update(update_json)
					if _update.update_id > telegram_bot_offset: telegram_bot_offset = _update.update_id
					# Traiter le message reçu
					telegram_bot_read_message(_update.message)
			else:
				print("-- telegram_bot_telegram_get_updates(): Error %s" % "There has been an unknown error")
		else:
			print("-- telegram_bot_get_updates(): Error %s" & "There has been an unknown error.")
#
def telegram_bot_send_message(chat_id, text, reply_to_message_id = None, reply_markup = None):
	# Options
	#	chat_id
	#	text
	#	disable_web_page_preview
	#	reply_to_message_id
	#	reply_markup
	head_data = {
		"chat_id": chat_id,
		"text": text
	}
	if reply_to_message_id != None:
		head_data.update([("reply_to_message_id", reply_to_message_id)])
	if reply_markup != None:
		head_data.update([("reply_markup", reply_markup)])
	# print("-- send_message(): head_data = %s" % head_data)
	#
	req = requests.post(url = "%s%s%s" % (telegram_bot_request, telegram_bot_token, "/sendMessage"), data = head_data)
	if (req.status_code != 200):
		print("-- send_message(): Error %s" % req.status_code)
	else:
		req_json = req.json()
		# print(req_json)
		#TODO: Verify if send message is equal to received message
#
def telegram_bot_read_message(message):
	# print("reading message %s" % message.message_id)
	# Checking message type
	if telegram_types.get("text") in message.type:
		telegram_bot_handle_message_text(message)
	elif telegram_types.get("new_chat_participant") in message.type:
		telegram_bot_handle_message_chat_participant_new(message)
	elif telegram_types.get("left_chat_participant") in message.type:
		telegram_bot_handle_message_chat_participant_left(message)
	elif telegram_types.get("new_chat_title") in message.type:
		telegram_bot_handle_message_chat_title_new(message)
	elif telegram_types.get("group_chat_created") in message.type:
		telegram_bot_handle_message_group_chat_created(message)
	elif telegram_types.get("photo") in message.type:
		telegram_bot_handle_message_picture(message)
	else:
		print("-- read_message(): Message type unhandled")
#
def telegram_bot_send_file(chat_id, file_name, reply_to_message_id = None, reply_markup = None, file_name_suppl = '', file_ext = '.txt'):
	head_data = {
		"chat_id": chat_id
		}
	if reply_to_message_id != None:
		head_data.update([("reply_to_message_id", reply_to_message_id)])
	if reply_markup != None:
		head_data.update([("reply_markup", reply_markup)])
	_file = {'document': (file_name + file_name_suppl + file_ext, open(file_name + file_ext, 'rb'), 'text/plain')}
	req = requests.get(url = "%s%s%s" % (telegram_bot_request, telegram_bot_token, "/sendDocument"), params = head_data, files = _file)
	if (req.status_code != 200):
		print("-- send_message(): Error %s" % req.status_code)
	else:
		req_json = req.json()
		print(req_json)
		#TODO: Verify if send message is equal to received message
#
#---------------------------------------------------------------
# Message handles
#---------------------------------------------------------------
def telegram_bot_handle_message_text(message):
	_to = ""; _from = ""
	_text = message.text
	if message.sender.id != message.chat.id:
		_to = "@%s" % message.chat.title
	if telegram_types.get("forward_from") in message.type:
		_from = " [fwd: %s]" % message.forward_from.first_name
		if _text[0] == "<":
			_from = " [fwd: %s]" % _text[1:].split(">")[0]
			_text = ' '.join(_text[1:].split(">")[1:])[1:]
	print("[#%s]\t<%s(%s)%s%s> %s" % (message.message_id, message.sender.first_name, message.sender.id, _to, _from, _text.encode("UTF-8")))
	# Handle commands
	# user / chat / command / arguments(full_text)
	if len(_text) > 2 and _text[0] == "/":
		if _to == "":
			# Privé
			_command = _text[1:].split()[0]
			_args = _text[1:].split()[1:]
			print("-- Private command is: %s | With args: %s" % (_command, _args))
			telegram_bot_command_user(_command, _args, message.sender, message.message_id)
		elif ("@" + telegram_bot_info.username.lower()) in _text.lower():
			# Groupe + Hilight
			# /command@Dj4xBot
			_bot_username = _text[1:].split('@')[1][:len(telegram_bot_info.username)].lower()
			#print("_bot_username = %s" % _bot_username)
			if _bot_username.lower() == telegram_bot_info.username.lower():
				_command = _text[1:].split('@')[0]
				_args = (" ".join(_text[1:].split('@')[1:])[len(_bot_username):]).split()
				print("-- Group command is: %s | With args: %s" % (_command, _args))
				telegram_bot_command_user(_command, _args, message.sender, message.message_id, message.chat)
		else:
			# Group /without hilight
			# /command [args]
			_command = _text[1:].split()[0]
			_args = _text[1:].split()[1:]
			print("-- Group command is: %s | With args: %s" % (_command, _args))
			telegram_bot_command_user(_command, _args, message.sender, message.message_id, message.chat)
	# LOGGER
	logged_groups = config.get("telegram_params").get("groups")
	_multi_line_text = _text.split('\n') # comment / uncomment for multi-line split support switch
	if message.chat.id.__str__() in logged_groups:
		for _line in _multi_line_text: # comment / uncomment for multi-line split support switch
			# _line = _text # delete if multi-line split support enabled
			_line = "%s | <%s%s> %s" % (time.strftime("%Y-%m-%d @ %H:%M:%S", time.gmtime(message.date)), message.sender.first_name, _from, _line)
			logger_file_add(logged_groups.get(message.chat.id.__str__()), _line)
#
def telegram_bot_handle_message_chat_participant_new(message):
	print("[#%s]\t** %s joined group %s" % (message.message_id, message.new_chat_participant.first_name, message.chat.title))
	if message.new_chat_participant.id != telegram_bot_info.id:
		telegram_bot_send_message(message.chat.id, "Hello, %s." % message.new_chat_participant.first_name, reply_to_message_id = message.message_id)
	else:
		telegram_bot_send_message(message.chat.id, "Salut tout le monde ! [chat #%s]" % message.chat.id, message.message_id)
def telegram_bot_handle_message_chat_participant_left(message):
	print("[#%s]\t** %s left group %s" % (message.message_id, message.left_chat_participant.first_name, message.chat.title))
	if message.left_chat_participant.id != telegram_bot_info.id:
		telegram_bot_send_message(message.chat.id, "Bye, %s." % message.left_chat_participant.first_name, reply_to_message_id = message.message_id)
def telegram_bot_handle_message_chat_title_new(message):
	print("[#%s]\t** Group %s changed title to ""%s""" % (message.message_id, message.chat.id, message.new_chat_title))
def telegram_bot_handle_message_group_chat_created(message):
	print("[#%s]\t** Group chat ""%s"" created" % (message.message_id, message.chat.title))
	telegram_bot_send_message(message.chat.id, "Salut tout le monde !")
def telegram_bot_handle_message_audio(message):
	print("Sorry, I can't hear audio for now.")
def telegram_bot_handle_message_document(message):
	print("Sorry, I can't download files for now.")
def telegram_bot_handle_message_picture(message):
	print("Sorry, I can't see pictures for now.")
	_to = ''
	if message.sender.id != message.chat.id:
		_to = "@%s" % message.chat.title
	else:
		_to = "@%s" % message.sender.first_name
	#print("telegram_bot_handle_message_picture(message):\n\t\tmessage.photo = %s" % message.photo)
	# LOGGER
	logged_groups = config.get("telegram_params").get("groups")
	if message.chat.id.__str__() in logged_groups:
		_thumb = telegram_classes_PhotoSize(message.photo[0])
		_picture = telegram_classes_PhotoSize(message.photo[1])
		# file size
		_picture_size = float(_picture.file_size)
		# units = {
			# 0: {
				# "unit": "octets", 
				# "level": (10 ** (3 * 0))
			# }
			# 1: {
				# "unit": "ko", 
				# "level": (10 ** (3 * 1))
			# }
			# 2: {
				# "unit": "Mo", 
				# "level": (10 ** (3 * 2))
			# }
			# 3: {
				# "unit": "Go", 
				# "level": (10 ** (3 * 3))
			# }
		# if _picture_size >  units[1]["level"] * 0.75:
			# _unit = units[1]["unit"]
			# _picture_size = _picture_size / units[1]["level"]
		# elif _picture_size >  units[2]["level"]:
			# _unit = units[2]["unit"]
			# _picture_size = _picture_size / units[2]["level"]
		# elif _picture_size >  units[3]["level"]:
			# _unit = units[3]["unit"]
			# _picture_size = _picture_size / units[3]["level"]
		# else:
			# _unit = units[0]["unit"]
			# _picture_size = _picture_size / units[0]["level"]
		units = ["octets", "ko", "Mo", "Go"]
		for i in range(4):
			if _picture_size >  (10 ** (3 * i)) * 0.75:
				_unit = units[i]
				_picture_size_new = "%.2f %s" % ((_picture_size / (10 ** (3 * i))), _unit)
		_line = "* %s has sent a picture to the group. It has %s width, %s height for a size of %s. File unique identifier is: '%s'." % (message.sender.first_name, _picture.width, _picture.height, _picture_size_new, _picture.file_id)
		_line = "%s | %s" % (time.strftime("%Y-%m-%d @ %H:%M:%S", time.gmtime(message.date)), _line)
		logger_file_add(logged_groups.get(message.chat.id.__str__()), _line)
	print("%s: %s sent a picture." % (_to, message.sender.first_name))
#
def telegram_bot_handle_message_sticker(message):
	print("Sorry, I don't care about stickers for now.")
def telegram_bot_handle_message_video(message):
	print("Sorry, I can't watch videos for now.")
def telegram_bot_handle_message_contact(message):
	print("Sorry, I have nothing to do with this contact for now.")
def telegram_bot_handle_message_location(message):
	print("Sorry, I can't change location, nor look at it for now.")
def telegram_bot_handle_message_chat_photo_new(message):
	print("Sorry, I can't see chat photos for now.")
def telegram_bot_handle_message_chat_photo_delete(message):
	print("Sorry, I don't care about photos for now.")
#
def telegram_bot_telegram_bot_command_start(context):
	# Démarre le bot
	print("Started!")
def telegram_bot_command_about(context, original_message_id):
	# Fournit le texte d'à propos
	telegram_bot_send_message(context, "@%(name)s\n%(name)s version %(version)s\nPar @Jahus\nUtilisez /aide pour avoir la liste des commandes." % {"name": __name__, "version": __version__}, original_message_id)
def telegram_bot_command_user(msg, args, user, original_message_id, chat = None):
	global PAUSE
	global HALT
	if chat == None: chat = user
	cmd = msg.split()[0]
	# print("Received command '%s' with arguments '%s'." % (cmd, args))
	# telegram_bot_send_message(chat.id, "Received command '%s' with arguments '%s'." % (cmd, args), original_message_id)
	if cmd.lower() == "about":
		telegram_bot_command_about(chat.id, original_message_id)
	if cmd.lower() == "keskifichou":
		telegram_bot_send_message(chat.id, "Une vraie chaudasse !", original_message_id)
	# LOGGER
	# Switches logger on/off
	if cmd.lower() == "log_pause" and user.id in config.get("telegram_params").get("admins"):
		if chat.id.__str__() in config.get("telegram_params").get("groups"):
			channel = config.get("telegram_params").get("groups").get(chat.id.__str__())
			PAUSE.update([(channel, not PAUSE.get(channel))])
			if PAUSE.get(channel):
				action = "paused"
			else:
				action = "resumed"
			telegram_bot_send_message(user.id, "Logging '%s' %s" % (channel, action))
		else:
			telegram_bot_send_message(chat.id, "Sorry, %s, this channel is not logged." % (user.first_name), reply_to_message_id = original_message_id)
	if cmd.lower() == "bot_halt" and user.id in config.get("telegram_params").get("admins"):
		HALT = True
	if cmd.lower() == "get_log" and user.id in config.get("telegram_params").get("admins"):
		if chat.id.__str__() in config.get("telegram_params").get("groups"):
			channel = config.get("telegram_params").get("groups").get(chat.id.__str__())
			telegram_bot_send_file(user.id, channel + "_log", file_name_suppl = (" - %s" % (time.strftime("%Y-%m-%d @ %H-%M-%S", time.gmtime()))), file_ext = ".log")
		else:
			telegram_bot_send_message(chat.id, "Sorry, %s, this channel is not logged." % (user.first_name), reply_to_message_id = original_message_id)
#
telegram_bot_get_bot_info()
print("EoF@offset: %s" % telegram_bot_offset)
#
#---------------------------------------------------------------
# SCRIPT
#---------------------------------------------------------------
#+DEBUG
print("script is ok")
#/DEBUG
# Add lines to the file
def logger_file_add(channel, text):
	if not PAUSE.get(channel):
		log_file_name = channel + "_log.log"
		with open(log_file_name, mode = 'a+b', buffering = 1) as _file:
			# print(text, file = _file, flush = False)
			_file.write(bytes(text+"\r\n", encoding="UTF-8"))
#
# Turn around and check for new messages each timeout time
def logger_loop():
	while not HALT:
		#try:
		print("** logger_loop(): -- time: %s" % (time.strftime("%Y-%m-%d @ %H-%M-%S", time.gmtime())))
		telegram_bot_get_updates()
		#except:
		#	print("** ERROR ** logger_loop(): -- time: %s" % (time.strftime("%Y-%m-%d @ %H-%M-%S", time.gmtime())))
		timeout = config.get("telegram_params").get("timeout")
		time.sleep(float(timeout))
	telegram_bot_get_updates()
#
# Running script
logger_loop()
#
# EXITTING
print("* Script terminated")