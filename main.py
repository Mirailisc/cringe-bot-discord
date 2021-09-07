from shlex import join
import discord
from discord.ext import commands,tasks
import os
import asyncio
from dotenv import load_dotenv
import youtube_dl

load_dotenv()

intents = discord.Intents().all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="-", intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed  1 -reconnect_delay_max 5',
    'options': '-vn',
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send('You are not in a voice channel, you must be in a voice channel to run this command')
    else:
        channel = ctx.message.author.voice.channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

        voice.play(source)
        await ctx.send(f'**Now Playing: **{url}')

        while voice.is_playing():
            await asyncio.sleep(1)
        else:
            await voice.disconnect()
            print("Disconnected")

@client.command(pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot isn't in the voice channel.")

@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There's no music playing right now.")

@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("The music is still playing.")

@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(os.getenv("DISCORD_TOKEN"))
