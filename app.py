import discord
import os
import requests
import json

client = discord.Client()

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
  if message.content.startswith('..'):
    quote = get_quote()
    await message.channel.send(quote)

client.run("ODA5ODA3OTQxNTE0NTU5NTI4.YCaeag.1U3-zv5YLGN_EUwhKmJZUQ2k1Hk")
