import os
import json
import discord
import requests
from googletrans import Translator

client = discord.Client()

class Emios:
    author_id = 723074321383424040
    translator = Translator()
    will_translate = False
    channel_lang = []
    
    @staticmethod
    def channel_translation_setup(message):
        if message.content.startswith('--start') and message.author.id == Emios.author_id:        
            command_args = message.content.split(" ")
            Emios.channel_lang.append([message.channel, command_args[1].split("=")[1]])

        elif message.content.startswith('--stop') and message.author.id == Emios.author_id:
            for index, active in enumerate(Emios.channel_lang):
                if active[0] == message.channel:
                    Emios.channel_lang.pop(index)

        return None
    
    @staticmethod
    def translate(message):
        lang = "auto"
        if not message.author.bot and not message.author.id == Emios.author_id:
            for index, active in enumerate(Emios.channel_lang):
                if active[0] == message.channel:
                    lang = active[1]
                    return Emios.translator.translate(str(message.content), src=str(lang), dest="en").text
        
        return ""

    @staticmethod
    def force_translate(message):
        if message.author.id == Emios.author_id:
            if message.content.startswith("--translate"):
               command_args = message.content.split(" ")
               lang = str(command_args[1].split("lang=")[1])
               text = str(message.content[message.content.index("=")+3:])

               return Emios.translator.translate(text, src=lang, dest="en").text

        return ""
    
    @staticmethod
    def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        
        return(quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$inspire'):
        quote = Emios.get_quote()
        await message.channel.send(quote)

    Emios.channel_translation_setup(message)
    if Emios.translate(message):
        await message.channel.send(Emios.translate(message))

    if Emios.force_translate(message):
        await message.channel.send(Emios.force_translate(message))

client.run(os.getenv("DISCORD_BOT_TOKEN"))
