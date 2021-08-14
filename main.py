import discord
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
user = os.getenv("BLAME_USER")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author.id == user:
        await message.channel.send('<@%s> Cringe!' % user)

    if message.content.startswith('!cringe'):
        await message.channel.send('<@%s>' % user)

client.run(token)
