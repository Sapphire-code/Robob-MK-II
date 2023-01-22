# COPYRIGHT <sapphirekr> <2023>
import discord
from discord.ext import commands
import os
import sys
import datetime
from datetime import datetime
#import math
import cmath
import json
import urllib.request
import pyfiglet
from pyfiglet import figlet_format
from keep_alive import keep_alive
import openai
import requests
import random


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


@bot.command(name='meme')
async def meme(ctx):
  meme_list = ['funny', 'memes', 'dankmemes']
  random_sub = meme_list[random.randint(0, 2)]
  url = f"https://meme-api.com/gimme/{random_sub}"
  meme_img = json.loads(requests.request("GET", url).text)
  meme_large = meme_img["preview"][-3]
  await ctx.send(f"**Title:** {meme_img['title']}")
  await ctx.send(meme_large)
  


@bot.command(name='chat')
async def chat(ctx, *, args):
  user_query = ctx.message.content
  openai_api_key = os.getenv('OPENAI_API_KEY')
  response = openai.Completion.create(api_key=f'{openai_api_key}',
                                      model="text-davinci-003",
                                      prompt=user_query,
                                      temperature=0.5,
                                      max_tokens=500,
                                      top_p=0.3,
                                      frequency_penalty=0.5,
                                      presence_penalty=0.0)
  response_v = content = response['choices'][0]['text'].replace(
    str(user_query), "")
  embed = discord.Embed(title='AI Response', description=f"{response_v}")
  embed.set_footer(text='Made with OpenAI')
  await ctx.reply(embed=embed)


@bot.command(name='custom_embed')
async def custom_embed(ctx, title_c, description_c):
  embed = discord.Embed(title=f'{title_c}', description=f'{description_c}')
  await ctx.send(embed=embed)


@bot.command(name='text_art')
async def text_art(ctx, text):
  text = str(text)
  result = pyfiglet.figlet_format(text)
  await ctx.reply(f"```\n{result}\n```")


@bot.command(name='iss_location')
async def iss_location(ctx):
  iss_location = 'http://api.open-notify.org/iss-now.json'
  iss_people = 'http://api.open-notify.org/astros.json'
  response = urllib.request.urlopen(iss_location)
  data = json.loads(response.read())
  latitude = data['iss_position']['latitude']
  longtitude = data['iss_position']['longitude']
  timestamp = datetime.now()
  response_v = urllib.request.urlopen(iss_people)
  data_v = json.loads(response_v.read())
  people = data_v['number']
  #
  embed = discord.Embed(title='International Space Station Location',
                        description=f"""
    **Latitude:** {latitude}
    **longitude:** {longtitude}
    **Timestamp: ** {timestamp}
    **People on-board:** {people}
    *This location data is close but not exact since the ISS travels at a speed of 7.66km/s and only takes around 90 minutes to orbit around the earth*
    """,
                        color=discord.Colour.dark_blue(),
                        url='https://www.openstreetmap.org/?mlat=' +
                        str(latitude) + '&mlon=' + str(longtitude) +
                        '#map=3/' + str(latitude) + '/' + str(longtitude))
  embed.set_thumbnail(
    url=
    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/International_Space_Station_after_undocking_of_STS-132.jpg/2560px-International_Space_Station_after_undocking_of_STS-132.jpg'
  )
  await ctx.send(embed=embed)


# The code below is basically useless now due to the server info function.
"""
@bot.command(name='membercount')
async def membercount(ctx):
  embed = discord.Embed(
    title=('Member count'),
    description=(
      f'There are currently **{ctx.guild.member_count}** members in the server!'
    ),
    url=(''),
    timestamp=datetime.now(),
    color=discord.Colour.dark_blue())
  embed.set_footer(text=ctx.guild)
  embed.set_thumbnail(url='')
  await ctx.send(embed=embed)
  await ctx.message.delete()
"""


@bot.command(name='serverinfo')
async def showinfo(ctx):
  # await ctx.send(f'Server: {ctx.guild}')
  # await ctx.send(f'Channel: {ctx.message.channel}')
  # await ctx.send(f'Author: {ctx.author}')
  # await ctx.send(f'Message ID: {ctx.message.id}')
  embed = discord.Embed(title="Information On Server",
                        description=f"""
        **Server: **{ctx.guild}
        **#️⃣Channel: **{ctx.message.channel}
        **🆔Server ID: **{ctx.guild.id}
        **📆Created On: **{ctx.guild.created_at.strftime("%b %d %Y")}
        **👑Owner: **{ctx.guild.owner}
        **👥Members: **{ctx.guild.member_count}
        **💬Channel count: **{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice
        
        
        """)
  await ctx.send(content=None, embed=embed)


@bot.command(name='punch')
async def punch(ctx, *args):
  everyone = ', '.join(args)
  await ctx.send(f'**Punched** {everyone}')


@bot.command(name='showhelp')
async def showhelp(ctx):
  embed = discord.Embed(title="Help on Robob MK II bot",
                        description="functional commands.",
                        colour=discord.Colour.dark_blue())
  embed.add_field(name="$serverinfo",
                  value="Shows the info regarding the server")
  embed.add_field(name="$punch", value="punches the person you want")
  embed.add_field(name="$kick", value='kicks the person you want')
  embed.add_field(name='$slap', value='slaps the person you want')
  embed.add_field(name='$mathhelp', value='shows help on mathematics commands')
  embed.add_field(name='$iss_location', value='shows the location of the ISS')
  embed.add_field(name='$text_art',
                  value='converts your text prompt to text ascii art')
  embed.add_field(name='$custom_embed',
                  value='$custom_embed "title here" "description here"')
  embed.add_field(name='$chat', value='allows you to chat with an AI!')
  await ctx.send(content=None, embed=embed)


@bot.command(name='kick')
async def kick(ctx, *args):
  everybody = ", ".join(args)
  await ctx.send(f'**Kicked** {everybody}')


@bot.command(name='slap')
async def slap(ctx, *args):
  everyperson = ", ".join(args)
  await ctx.send(f'**Slapped** {everyperson}')


@bot.command(name='ban')
async def ban(ctx, *args):
  everyhuman = ", ".join(args)
  await ctx.send(f'**Banned** {everyhuman}')


@bot.command(name='mathhelp')
async def trighelp(ctx):
  embed = discord.Embed(
    title="Trigonometry Help",
    description="Shows help regarding trigonometry",
  )
  embed.add_field(
    name='$sin',
    value="Takes out the sine value of the expression given; for eg. $sin 90",
    inline=True)
  embed.add_field(
    name='$cos',
    value="Takes out the cosine value of the expression given; for eg. $cos 90",
    inline=True)
  embed.add_field(
    name='$tan',
    value="Takes out the tan value of the expression given; for eg. $tan 90",
    inline=True)
  embed.add_field(name='$solveQuad',
                  value='usage: $solvequad valuea valueb valuec')
  await ctx.send(content=None, embed=embed)


@bot.command(name='sin')
async def sin(ctx, num1):
  num1 = int(num1)
  solution = cmath.sin(num1)
  await ctx.send(solution)


@bot.command(name='cos')
async def cos(ctx, num1):
  num1 = int(num1)
  solution = cmath.cos(num1)
  await ctx.send(solution)


@bot.command(name='tan')
async def tan(ctx, num1):
  num1 = int(num1)
  solution = cmath.tan(num1)
  await ctx.send(solution)


@bot.command(name='solveQuad')
async def solveQuad(ctx, a, b, c):
  #await ctx.send(
  #  "The General Form is: ax²+bx+c, where a, b, and c are real numbers where a != 0, make sure to put it in this form exactly"
  # )
  b = int(b)
  a = int(a)
  c = int(c)
  just = ((b**2) - (4 * a * c))

  just = float(just)

  x = ((-1 * b) + cmath.sqrt(just))
  value_x = x / (2 * a)

  xv2 = ((-1 * b) - cmath.sqrt(just))
  value_xv2 = xv2 / (2 * a)

  if value_x == value_xv2:
    await ctx.send(f'x = {str(value_x)}')
  elif value_x != value_xv2:
    await ctx.send(f'x = {str(value_x).replace("j", "")} or {str(value_xv2).replace("j", "")}')


keep_alive()
# Running the bot
my_secret = os.environ['TOKEN']
try:
  bot.run(my_secret)
except:
  os.system("kill 1")
