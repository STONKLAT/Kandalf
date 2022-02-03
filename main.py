'''
Remember to not steal my code ;)
If you are being rate limited just type " kill 1 " in the replit shell

© 2022 Stonklat Corporation
'''

#Importing Required Modules
import discord
import os
import asyncio
from pytube import Search
import subprocess
from discord import embeds
from time import sleep
from os import system

import random
import pytube
from pytube import YouTube
import keep_alive
import nacl #<--- Dont delete important for downloading videos
import youtube_dl
import time
from discord.ext import commands,tasks
from data import responses
print("**DEBUG CONSOLE**")


#default status:
stet='AKA Kandalf the II'

#Main Prefix of the bot:
prefix='.'



client = commands.Bot(command_prefix=prefix)

client.remove_command('help')
#Bot Commands
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=stet), status=discord.Status.idle)
  system('clear')
  print("**DEBUG CONSOLE**")
  print("Bot Ready")
#==================#
@client.command(aliases=["bot_clean"])
async def cleanup(ctx):
  if ctx.message.author.id == 318365547156996096:
    async with ctx.typing():
      await ctx.send("Please confirm cleanup at the console.")
      takczynie=input('Are you sure you want to erase all mp3 files from the drive (y/n): ')
      if takczynie=='y' or takczynie=='Y':
        system('rm ./music/*.mp4')
        await ctx.send("Cleanup Complete")
        print('Cleanup Complete')
      else:
        await ctx.send('Cleanup aborted')
        print('Cleanup aborted')
  else:
    await ctx.send('You are not allowed to use this command')

@client.command()
async def say(ctx, *, text):
    message = ctx.message
    await message.delete()

    await ctx.send(f"{text}")

@client.command()
async def test(ctx):
  await ctx.send('**The Bot is Working!** <a:tick:801130706172510318>')


  

@client.command()
async def help(ctx):
  await ctx.send(f"{ctx.author.mention} is a crybaby and needs serious help!")
  channel = await ctx.author.create_dm()
  await channel.send("<a:obama_prism:937776312834195516> Serious help:\nhttps://bit.ly/KandalfCommands")


@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! **{round(client.latency * 1000)}ms** <:internetconnection:801129070636302337>')

@client.command(aliases=["8ball"])# .8ball command
async def _8ball(ctx, *, user_response='none'):
  if user_response=='none':
    random_response = random.choice(responses)
    await ctx.send(f"Answer: {random_response}")
  else:
    random_response = random.choice(responses)
    await ctx.send(f"Question: {user_response}\nAnswer: {random_response}")

@client.command(aliases=['api.stop.python.script', 'bot_stop'])
async def apistoppythonscript(ctx):
  await ctx.send('<a:loading:926170861982072902> **Stopping the main python script...**')
  time.sleep(1)
  await ctx.send('<:python:926172991698636852> **The Script has been terminated succesfully!**')
  exit()

@client.command()
async def status(ctx, *, stat):
  await client.change_presence(activity=discord.Game(name=stat))  
  await ctx.send(f'**My status is now** {stat}')
#----------------Tools-------------------

@client.command()
async def embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    await ctx.channel.purge(limit=1)
    information = await ctx.send(f'🪄 Embed Creation wizard! Just follow the steps!\nType "cancel" to Cancel the setup.')
    ask_title = await ctx.send('**Provide a title:**')
    title = await client.wait_for('message', check=check)
    if title.content=='cancel' or title.content=='Cancel':
      await ask_title.delete()
      await title.delete()
      await information.delete()
      await ctx.send('Setup Cancelled', delete_after=5)
      return
  
    ask_desc = await ctx.send('**Provide a description:**')
    desc = await client.wait_for('message', check=check)

    if desc.content=='cancel' or desc.content=='Cancel':
      await ask_title.delete()
      await ask_desc.delete()
      await desc.delete()
      await title.delete()
      await information.delete()
      await ctx.send('Setup Cancelled', delete_after=5)
      return
    
    embed = discord.Embed(title=title.content, description=desc.content, color=0x0b8bfb)
    await title.delete()
    await information.delete()
    await desc.delete()
    await ask_desc.delete()
    await ask_title.delete()
    wait_con = await ctx.send('<a:loading:926170861982072902> Creating your embed...')
    sleep(1.5)
    await wait_con.delete()
    await ctx.send(embed=embed)




@client.command(aliases=['about'])
async def kandalf(ctx):
  embed = discord.Embed(title=f'Hello, {ctx.author.name} i am Kandalf!', description='Multifunctional but mainly a music bot. Which has lots of features.', color=0x0b8bfb)
  file = discord.File("./image.png", filename="image.png")
  embed.set_image(url="attachment://image.png")
  await ctx.send(file=file, embed=embed)

#-----------------Moderation------------------------

#clear command
@client.command(aliases=['clear'])
async def purge(ctx, amount=0):
  await ctx.channel.purge(limit=amount+1)


@client.command() #Kicking Members
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  if reason == None:
    await ctx.send(f'**{member}** has been kicked')
  else:
    await ctx.send(f'**{member}** has been kicked for {reason}')
@client.command() #Banning members
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  if ctx.message.author.guild_permissions.administrator:
    print(member, 'has been banned')
    if reason == None:
      await ctx.send(f'**{member}** has been banned')
    else:
      await ctx.send(f'**{member}** has been Banned for {reason}')
  else:
    ctx.send('Permission Denied')
@client.command() #unbanning members
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      print('unbanned', user)
      return
@client.command()
async def update(ctx):
  random_number = random.randint(1,10)
  await ctx.send('<:internetconnection:801129070636302337> **Checking for updates...**')
  time.sleep(random_number)
  await ctx.send('<a:tick:801130706172510318> **No updates found!**')

@client.command(aliases=['amongus'])
async def amogus(ctx):
  for i in range(100):
    await ctx.send('<a:Amongus_Distracted:926556352585793537>', delete_after=10)


    
#----------------Music section---------------------

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
  try:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("<:clowncrywonky:936305409621393418> The bot is not connected to a voice channel.")
  except:
    await ctx.send("<:clowncrywonky:936305409621393418> The bot is not connected to a voice channel.")

@client.command(name='url')
async def url(ctx, *, url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            msg = await ctx.reply("**Keep in mind that Fetching may take some time. I will try shorting it in some future update.**\n<a:loading:926170861982072902> Fetching song...")
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path="./music")
            voice_channel.play(discord.FFmpegPCMAudio(source=out_file))
            logs = open("music/songs.log", "a")
            logs.write(f"{ctx.message.author.name} is playing {yt.title} url: {url}\n")
            logs.close()
            await msg.edit(content='<:Patrick_Winner:936303561640378379> **Now playing:** {}'.format(yt.title))
    except:
        await ctx.send("<:clowncrywonky:936305409621393418> The bot is not connected to a voice channel.")


@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("<:clowncrywonky:936305409621393418> Nothing is being played at the moment")
    
@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("<:clowncrywonky:936305409621393418> The bot was not playing anything before this. Use play or search command")

@client.command(name='stop', help='Stops the song')
async def stop(ctx):
  if ctx.message.guild.voice_client.is_playing():
    voice_client = ctx.message.guild.voice_client
    await voice_client.stop()
  else:
    await ctx.send("<:clowncrywonky:936305409621393418> Nothing is being played at the moment")

#Volume work in progress
'''
@client.command(name='volume', help='This command changes the bots volume')
async def volume(ctx, volume: int):
  try:
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")
    if volume>200:
      return await ctx.send("Maximum volume is 200")
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")
  except:
    await ctx.send("yo! mate the value you've entered is not valid mate! try again!")
'''
@client.command()
async def volume(ctx):
  await ctx.send('🪄 This command is work in progress!')


@client.command(aliases=['search'])
async def play(ctx, *, wat):
        s = Search(wat)
        result=str(s.results[0])

        result_2=result[41:80]

        result_3=f'https://www.youtube.com/watch?v={result_2}'

        result_final=result_3
        print(result_3)


        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            msg = await ctx.reply(f"**Keep in mind that Fetching may take some time. I will try shorting it in some future update.**\n<a:loading:926170861982072902> Fetching song...")
            yt = YouTube(result_final)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path="./music")
            voice_channel.play(discord.FFmpegPCMAudio(source=out_file))
            logs = open("music/songs.log", "a")
            logs.write(f"\n{ctx.message.author.name} is playing {yt.title} url: {result_final}\n")
            logs.close()
            await msg.edit(content='<:Patrick_Winner:936303561640378379> **Now playing:** {}'.format(yt.title))


#--------------------------------------
    
######################################

keep_alive.keep_alive() #Makes the bot 24/7
client.run(os.getenv("TOKEN")) #Finally run the bot