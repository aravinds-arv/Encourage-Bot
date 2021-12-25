import os
import discord
import json
import requests
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()
token = os.environ['TOKEN']

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
starter_encouragements = [
  'Cheer Up!!',
  'Hang in there..',
  'You are a great person/bot!!'
]

if 'responding' not in db.keys():
  db['responding'] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_response = json.loads(response.text)
  quote = json_response[0]['q'] + " -" + json_response[0]['a']
  return quote

def update_encouragements(encouraging_msg):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_msg)
  else:
    db['encouragements'] = [encouraging_msg]

def delete_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  options = starter_encouragements
  if "encouragements" in db.keys():
    options.extend(db["encouragements"])

  if db['responding']:
    if msg.startswith('>hello'):
      await message.channel.send('Hello!')

    if msg.startswith('>inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('>new'):
    encouraging_msg = msg.split('>new ', 1)[1]
    update_encouragements(encouraging_msg)
    await message.channel.send('New encouraging message added!')

  if msg.startswith('>del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('>del', 1)[1])
      delete_encouragements(index)
      encouragements = db['encouragements']
      await message.channel.send(list(encouragements))

  if msg.startswith('>list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
      await message.channel.send(list(encouragements)) 

  if msg.startswith('>toggle_response'):
    if db['responding']:
      db['responding'] = False
      await message.channel.send('Bot response turned off')
    else:
      db['responding'] = True
      await message.channel.send('Bot response turned on')

keep_alive()
client.run(token)
