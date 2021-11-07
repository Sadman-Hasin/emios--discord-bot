import os
import discord
from googletrans import Translator
from hadith import Hadith

emios = discord.Client()

class Emios:
	translator = Translator()

	@staticmethod
	def reverse_message(message):
		return message.channel.send(f"Reversed Message: {message.content[::-1]}")

	@staticmethod
	def translate(message):
		args = message.content.split("! ")[0]
		msg = message.content.split("! ")[1]

		try:
			arg_from = args.find("from=")
			arg_to = args.find("to=")

			src = args[arg_from+len("from="):arg_from+len("from=")+2]
			dest = args[arg_to+len("to="):arg_to+len("to=")+2]


			translation = Emios.translator.translate(msg, src=src, dest=dest)
		
		except Exception as error:
			translation = Emios.translator.translate(msg)

		return message.channel.send(f"Translation: {translation.text}")
	
	@staticmethod
	def getHadith(message):
		hadith = Hadith.fetch_random()
		collection = hadith[2]["collection"]

		chapterNumber = hadith[2]["hadith"][0]["chapterNumber"]
		chapterTitle = hadith[2]["hadith"][0]["chapterTitle"]
		raw_hadith_body = hadith[2]["hadith"][0]["body"]
		hadith_body = raw_hadith_body[3:raw_hadith_body.find("<br/><br/><b>")]
		hadith_book = raw_hadith_body[raw_hadith_body.find("<br/><br/><b>")+len("<br/><br/><b>"):raw_hadith_body.find("</b>.<br/><br/></p>")]
		body = f"{hadith_body}\n{hadith_book}"

		return message.channel.send(f"Collection: {collection.capitalize()}\n\nChapter title: {chapterTitle}\nChapter number: {chapterNumber}\n\n{body}")

	
@emios.event
async def on_message(message):
	if message.author == emios.user:
		return

	if message.content.startswith("r! "):
		await Emios.reverse_message(message)

	elif message.content.startswith("translate ") or message.content.startswith("translate!"):
		await Emios.translate(message)
	
	elif message.content.startswith("hadith!"):
		await Emios.getHadith(message)
        
emios.run(os.getenv("DISCORD_BOT_TOKEN"))


