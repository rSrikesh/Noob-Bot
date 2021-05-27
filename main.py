import os
import discord
import requests
import json
from keep_alive import keep_alive
import random

intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents=intents)
my_secret = os.environ['token']


def get_quote():

  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def facts():
  response = requests.get("http://numbersapi.com/random?json")
  json_data = json.loads(response.text)
  return json_data['text']

def memes():
  response = requests.get("https://v2.jokeapi.dev/joke/Any/type=single")
  json_data = json.loads(response.text)
  return json_data['joke']

def two_memes():
  response = requests.get("https://v2.jokeapi.dev/joke/Any?type=twopart")
  json_data = json.loads(response.text)
  return json_data['setup'],json_data['delivery']

def ani_quotes():
  response = requests.get("https://animechan.vercel.app/api/random")
  json_data = json.loads(response.text)
  return json_data['anime'],json_data['character'],json_data['quote'] 

def one_piece_chap():
  x = random.randint(1, 1000)
  url = "https://onepiececover.com/api/chapters/"+str(x)
  response = requests.get(url)
  json_data = json.loads(response.text)
  return json_data['title'],json_data['chapter'],json_data['summary']


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
  guild = client.get_guild(808380934553993278)
  channel = guild.get_channel(808380936651407362)
  await channel.send(f'Welcome to the Server {member.mention}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('>hello'):
    await message.channel.send('Have a nice day!!')
  
  if message.content.startswith('>inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('>fact'):
    fact = facts()
    await message.channel.send(fact)

  if message.content.startswith('>meme'):
    meme = memes()
    await message.channel.send(meme)

  if message.content.startswith('>2meme'):
    meme1,meme2 = two_memes()
    await message.channel.send(meme1)
    await message.channel.send(meme2)

  if message.content.startswith('>quote'):
    quote1,quote2,quote3 = ani_quotes()
    final_quote_1 = "Anime: "+quote1
    final_quote_2 = "Character: "+quote2
    final_quote_3 = "Quote: "+quote3
    await message.channel.send(final_quote_1)
    await message.channel.send(final_quote_2)
    await message.channel.send(final_quote_3)
  
  if message.content.startswith('>chap'):
    title,chapter,summary = one_piece_chap()
    await message.channel.send(title)
    await message.channel.send(chapter)
    await message.channel.send(summary)

keep_alive()
client.run(my_secret)


