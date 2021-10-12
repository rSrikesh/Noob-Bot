import os
import discord
import requests
import json
from keep_alive import keep_alive
import random
import praw

my_secret = os.environ['token']
clientid = os.environ['c_id']
secret = os.environ['c_secret']
u_name = os.environ['u_name']
p_word = os.environ['pword']
usr_agent = os.environ['u_agent']

reddit = praw.Reddit(client_id = clientid ,
                     client_secret=secret,
                     username=u_name,
                     password=p_word,
                     user_agent=usr_agent,
                     check_for_async=False)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents,status=discord.Status.do_not_disturb)

def get_quote():

  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def facts():
  response = requests.get("http://numbersapi.com/random?json")
  json_data = json.loads(response.text)
  return json_data['text']

def meme(category):
    subreddit = reddit.subreddit(category)
    all_subs = []
    top = subreddit.top(limit = 300)

    for submission in top:
      all_subs.append(submission)
    
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title=name)
    em.set_image(url = url)
    return em


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
  guild = client.get_guild(808380934553993278)
  channel = guild.get_channel(808380936651407362)
  await channel.send(f'Welcome to the Server {member.mention}')

@client.event
async def on_member_remove(member):
  guild = client.get_guild(808380934553993278)
  channel = guild.get_channel(808380936651407362)
  await channel.send(f'See You Soon {member.mention}')

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
    em = meme("Meme")
    await message.channel.send(embed = em)
  
  if message.content.startswith('>fp'):
    em1 = meme("Facepalm")
    await message.channel.send(embed = em1)
      
keep_alive()
client.run(my_secret)
