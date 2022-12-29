import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import os
import asyncio
import time
import random
import json
import subprocess
from data import *

from youtube_dl import YoutubeDL
import youtube_dl
import nacl
import ffmpeg
import validators

# Make a file called "details.py" in the same directory as main.py
# and in that file set the variable "token" to your discord bot token
# and Owner_ID to your discord profile Id
from details import token, Owner_ID

print('**DEBUG CONSOLE**')

# Default status:
Bot_Status='amazing music!'

# Main Prefix of the bot:
prefix='.'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

unsupported = '```fix\nPlease note that this command is not supported and may not even work\n```'

client.remove_command('help')

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=Bot_Status), status=discord.Status.idle)
  print("Bot Ready")

# ====================> Commands section

@client.command()
@has_permissions(manage_messages=True)
async def say(ctx, *, text):
    message = ctx.message
    if ctx.message.author.id == Owner_ID:
      await message.delete()
      await ctx.send(f"{text}")
    else:
      if "@" in text:
        await message.reply('The use of the "@" is not allowed')
        return
      elif "#" in text:
        await message.reply('The use of the "#" is not allowed')
        return
      await message.delete()
      await ctx.send(f"{text}")
@say.error
async def say_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you need Manage messages perission to do that!".format(ctx.author.mention)
        await ctx.send(text)


@client.command()
async def help(ctx):
  await ctx.send(f"{ctx.author.mention} is a crybaby and needs serious help!")

@client.command(aliases=['dm'])
async def send_msg(ctx, who: discord.Member, *, what):
  if ctx.message.author.id == Owner_ID:
    await ctx.channel.purge(limit=1)
    try:
      await who.send(what)
      await ctx.send(f'Succesfully sent {what} to {who.name}', delete_after=2)
    except:
      await ctx.send('Error')
  else:
    return

@client.command()
async def ping(ctx):
  await ctx.send(f'🏓 Pong! **{round(client.latency * 1000)}ms** <:internetconnection:801129070636302337>')


@client.command(aliases=["8ball"])
async def _8ball(ctx, *, user_response='none'):
  if user_response=='none':
    random_response = random.choice(responses)
    await ctx.send(random_response)

  else:
    random_response = random.choice(responses)
    await ctx.send(f"Question: {user_response}\nAnswer: {random_response}")



@client.command()
async def status(ctx, *, stat):
  if not ctx.message.author.id == Owner_ID:
    return
  await client.change_presence(activity=discord.Game(name=stat))  
  await ctx.send(f'**My status is now** {stat}')


@client.command(aliases=['clear'])
@has_permissions(manage_messages=True)
async def purge(ctx, amount=0):
  await ctx.channel.purge(limit=amount+1)
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.author.mention)
        await ctx.send(text)


@client.command()
@has_permissions(manage_webhooks=True) 
async def embed(ctx, edit='no', id='no'):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    await ctx.channel.purge(limit=1)
    colour=0x0b8bfb
    if edit=='edit':
      if id=='no':
        await ctx.send('No message id provided!\nNext time try: `.embed edit <id>`. ld ', delete_after=5)
      else:
        msg = await ctx.fetch_message(id)
        ask_new_title = await ctx.send('**Provide a new title:**')
        new_title = await client.wait_for('message', check=check)

        ask_new_desc = await ctx.send('**Provide a new description:**')
        new_desc = await client.wait_for('message', check=check)

        new_embed = discord.Embed(title=new_title.content, description=new_desc.content, color=colour)

        await new_title.delete()
        await new_desc.delete()
        await ask_new_desc.delete()
        await ask_new_title.delete()
        wait_con = await ctx.send('<a:loading:926170861982072902> Editing your embed...')
        time.sleep(1)
        await wait_con.delete()
        await msg.edit(embed=new_embed)
    
    elif edit=='no' or edit=='backrooms':
      if edit=='backrooms':
        colour=0x947742
      information = await ctx.send(f'🪄 Embed Creation wizard! Just follow the steps!\nTo edit an embed type `.embed edit <message id>`\nType `cancel` to Cancel the setup.')
      ask = await ctx.send('```Provide a title```')
      title = await client.wait_for('message', check=check)
      if title.content=='cancel' or title.content=='Cancel':
        await ask.delete()
        await title.delete()
        await information.delete()
        await ctx.send('Setup Cancelled', delete_after=5)
        return
      await title.delete()

      await ask.edit(content='```Provide a description```')
      desc = await client.wait_for('message', check=check)

      if desc.content=='cancel' or desc.content=='Cancel':
        await ask.delete()
        await desc.delete()
        await title.delete()
        await information.delete()
        await ctx.send('Setup Cancelled', delete_after=5)
        return
    
      embed = discord.Embed(title=title.content, description=desc.content, color=colour)
      await information.delete()
      await desc.delete()
      await ask.edit(content='<a:loading:926170861982072902> `Loading` ```Compiling Your Embed```')
      time.sleep(1.5)
      await ask.delete()
      await ctx.send(embed=embed)
    else:
      await ctx.send('Not a valid command', delete_after=5)
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.author.mention)
        await ctx.send(text)

@client.command(aliases=["server"])
async def linux(ctx, *, command):
    if not ctx.message.author.id == Owner_ID:
      return
    
    ERROR = None
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    if command.lower() == "terminal":
      terminalActive = True
      terminalContent = '```bash\n"Welcome to the Linux terminal!"\n"Please use the "§" character instead of a space in commands"\n"Write "exit" to leave the terminal"\n```'
      terminal = await ctx.reply(terminalContent)
      while terminalActive:
        userCmd = await client.wait_for('message', check=check)
        await userCmd.delete()
        if userCmd.content.lower() == 'exit': 
          await terminal.edit(content="```[Session ended]```", delete_after=5)
          await ctx.message.delete()
          return

        try:
          result = subprocess.run(userCmd.content.split('§'), stdout=subprocess.PIPE).stdout.decode('utf-8')
          
          if result == '': result = "\n"

          terminalContent = f"\n{terminalContent[:-3]}{result}```"
          await terminal.edit(content=f"\n{terminalContent}")

        except Exception as e:
          error_message = str(e)
          i = error_message.find('\n')
          error_message_discord = error_message[:i+1] + "- " + error_message[i+1:]
          error_message_discord = f"```diff\n{error_message_discord}\n```"
          await ctx.send(error_message_discord, delete_after=10)
        


    await ctx.send(f"{unsupported[:-3]}Please use '.linux terminal' instead\n```")    
    try:
      result = subprocess.run(command.split(), stdout=subprocess.PIPE)
      result = result.stdout.decode('utf-8')
      if result == '': await ctx.send("Success!")
      await ctx.send(f'```bash\n{result}\n```')
    except Exception as e:
      error_message = str(e)
      await ctx.send(f'```\n{error_message}\n```')
      
    

# ==========> Music Player Section

global looping
looping = []

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

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
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name='leave', aliases=['left'])
async def leave(ctx):
  try:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("<:clowncrywonky:936305409621393418> The bot is not connected to a voice channel.")
  except:
    await ctx.send("<:clowncrywonky:936305409621393418> The bot is not connected to a voice channel.")

@client.command(name='stop', help='Stops the song')
async def stop(ctx):
  if ctx.message.guild.voice_client.is_playing():
    voice_client = ctx.message.guild.voice_client
    voice_client.stop()
  else:
    await ctx.send("<:clowncrywonky:936305409621393418> Nothing is being played at the moment")

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
        await ctx.send("<:clowncrywonky:936305409621393418> The bot was not playing anything before this. Use the pause command first!")

@client.command(aliases=['radio'])
async def stream(ctx, url=None):
 
  Stations = {
    "heart": "https://media-ssl.musicradio.com/HeartLondon",
    "herts": "https://media-ssl.musicradio.com/HeartWatford",
    "world": "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "RMFFM": "https://rs203-krk.rmfstream.pl/RMFFM48?aw_0_req.gdpr=true",
    "RMFMAXX": "https://rs203-krk.rmfstream.pl/RMFMAXXX48?aw_0_req.gdpr=true",
    "Anty": "https://n-12-1.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5",
    "BBC1": "https://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
    "BBC2": "https://stream.live.vc.bbcmedia.co.uk/bbc_radio_two"
  }
  if url == "stations":
    await ctx.send(f"```python\nStations = {json.dumps(Stations, indent=2, default=str)}\n```")
    return

  try: await ctx.message.author.voice.channel.connect()
  except: pass

  text = "Syntax: `.stream <raw url>` or `.stream <radio station choosen from list>`\n```Available radio stations:```\nDefault: **BBC World Service**, International `.stream world`\n1. **Heart**, United Kingdom `.stream heart`\n2. **BBC Radio 1**, United Kingdom `.stream BBC1`\n3. **BBC Radio 2**, United Kingdom `.stream BBC2`\n4. **RMF fm**, Poland `.stream RMFFM`\n5. **RMF MAXX**, Poland `.stream RMFMAXX`\n6. **Anty Radio**, Poland `.stream Anty`"

  gg = ctx.message.guild.voice_client
  if url == None:
    await ctx.send(text)
    return
  else:
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    try: ctx.message.guild.voice_client.stop()
    except: pass
    loading = await ctx.send("<a:spin:1012720456954028042> Loading...")
    try:
      gg.play(discord.FFmpegPCMAudio(source=Stations[url]))
      await loading.edit(content=f'<:Patrick_Winner:936303561640378379> Now Playing **__{url}__**')
    except:
      if not validators.url(url):
        await loading.edit(content=f'<:Patrick_Cry:1012721642750873620> Please enter a radio station from the list, or a url leading to an mp3 file')
        return
      try:
        gg.play(discord.FFmpegPCMAudio(url))
        await loading.edit(content=f'<:Patrick_Winner:936303561640378379> Playing!')
      except:
        await loading.edit(content=f'<:Patrick_Cry:1012721642750873620> There was a problem')

# Player Class
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.7):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.command()
async def play(ctx, *, url):
  global looping
  ID = ctx.message.guild.id
  try: await ctx.message.author.voice.channel.connect()
  except: pass
  if ctx.message.guild.voice_client.is_playing():
    await ctx.send('There is something playing right now, Please use `.stop` before playing something else.')
    return
  
  yt_icon = False

  message = await ctx.reply(f'<a:spin:1012720456954028042> **Loading...**')

  async def loop(guild, voice, audio):
    if ctx.message.guild.voice_client.is_playing(): return
    print('*  Running loop function')
    if ID in looping:
      voice.play(audio)

  if validators.url(url):
    info_dict = ytdl.extract_info(url, download=False)
    video_title = info_dict.get('title', None)
    if "youtu" in url: yt_icon = True
    await message.edit(content=f'<a:spin:1012720456954028042> **Buffering `{video_title}`...**')
  else:
    yt_icon = True
    await message.edit(content=f'<a:spin:1012720456954028042> **Searching for `{url}`...**')
  
  try:
    player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
  except:
    await ctx.send ('<:Patrick_Cry:1012721642750873620> Player error')
    print('\033[1;31;40mPlayer error (Line: 319)')
    return

  try:
    ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(loop(ctx.guild, ctx.voice_client, player), client.loop))
    if yt_icon==True: await message.edit(content=f'<:Patrick_Winner:936303561640378379> <:youtube:801865130676846623> **Now playing:** `{player.title}`')
    else: await message.edit(content=f'<:Patrick_Winner:936303561640378379> **Now playing:** `{player.title}`')
  except:
    await message.edit(content=f'<:Patrick_Cry:1012721642750873620> There was a problem')

@client.command()
async def loop(ctx, status="None"):
  await ctx.send(unsupported)
  global looping
  ID = ctx.message.guild.id

  if status == "status" or status == "?":
    if ID in looping: await ctx.send("Looping is Enabled!")
    else: await ctx.send('Looping is Disabled')
    return

  if ID in looping:
    looping.remove(ID)
    await ctx.reply("Looping Disabled!")
  else:
    looping.append(ID)
    await ctx.reply("Looping Enabled")

# ====================> Events

'''
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
'''

# ====================> Start The bot
client.run(token)