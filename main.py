import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
user = 349193980602220546

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.content.startswith('-cringe'):
        if message.author.id == user:
            await message.channel.send('<@%s> You!' % user)
        else:
            await message.channel.send('<@%s>' % user)
    
    if message.author.id == user:
        await message.channel.send('<@%s> Cringe!' % user)

client.run(os.getenv("DISCORD_TOKEN"))
