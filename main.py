import os
import discord
from keep_alive import keep_alive
import random
import praw
from discord.ext import commands

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

client = commands.Bot(intents=intents,status=discord.Status.do_not_disturb,command_prefix = ">")

def meme(category):
    subreddit = reddit.subreddit(category)
    all_subs = []
    top = subreddit.top(limit = 35)

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

@client.command(aliases=['h'])
async def hello(ctx):
  await ctx.send("Hello")

@client.command()
async def dank(ctx,*,subreddit):
  em = meme(str(subreddit))
  await ctx.send(embed=em)

@client.command(aliases=['b'])
async def ban(ctx,member:discord.Member, *,reason=None):
  await member.ban(reason=reason)

@client.command()
async def avatar(ctx,member: discord.Member):
  url = member.avatar_url
  em = discord.Embed()
  em.set_image(url=url)
  await ctx.send(embed=em)

keep_alive()
client.run(my_secret)



