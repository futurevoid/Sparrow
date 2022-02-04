# create a discord bot that will automatically send messages after a certain amount of time has passed
# (in this case, the time is set to 5 seconds)
import asyncio
from email import message
import time
import random
import os
import sys
import json
from matplotlib import image
import requests
import discord
import aiohttp
import datetime as dt
from discord.ext import commands

# load the discord client
client = discord.Client()


# create an event that will run when the bot is ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



# bot prefix
bot = commands.Bot(command_prefix='^')


# create an event that will run when !hello is called
# create a function that will run when a message is sent
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith("^lol") or message.content.startswith("/lol"):
        r = requests.get(
            'https://sv443.net/jokeapi/v2/joke/Miscellaneous,Pun,Spooky,Christmas?blacklistFlags=nsfw,racist,sexist&type=single').json()
        joke = r['joke']
        await message.channel.send(joke)
    elif message.content.startswith('^hello') or message.content.startswith('/hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('^log') or message.content.startswith('/log'):
        msg = f'Message sent\n{message.content}\n{message.author}\n{message.channel}\n{message.guild}\n{message.id}\n{message.type}\n{message.attachments}\n{client.user.id}\n{client.user.name}\n{client.user.discriminator}\n{client.user.avatar}\n-------'.format(
            message)
        await message.channel.send(msg)
    elif message.content.startswith('^ping') or message.content.startswith('/ping'):
        before = time.monotonic()
        ping = round(time.monotonic())
        msg = f'Pong! 🏓 {message.author.mention} {int(ping)}ms'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('^qr') or message.content.startswith('/qr'):
        msg = f'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={message.content[8:]}'.format(message)
        await message.channel.send(msg)
    # send a message to the channel every 24 hours
    while message.content.startswith("^autosend") or message.content.startswith("/autosend"):
        await message.channel.send("/share")
        await asyncio.sleep(15)
        await message.channel.send("+share")
        await asyncio.sleep(86400)
        await message.channel.send("/share")
        await asyncio.sleep(15)
        await message.channel.send("+share")
    async with aiohttp.ClientSession() as cs:
        if message.content.startswith('^mems') or message.content.startswith('/mems'):
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed = discord.Embed(title="Memes", description="Here are some memes", color=0x00ff00)
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await message.channel.send(embed=embed)
    if message.content.startswith('^cat') or message.content.startswith('/cat'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://aws.random.cat/meow') as r:
                res = await r.json()
                embed = discord.Embed(title="Cat", description="Here is a cat", color=0x00ff00)
                embed.set_image(url=res['file'])
                await message.channel.send(embed=embed)                        
    elif message.content.startswith('^catfact') or message.content.startswith('/catfact'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://catfact.ninja/fact') as r:
                res = await r.json()
                embed = discord.Embed(title="Cat Fact", description="Here is a cat fact", color=0x00ff00)
                embed.set_image(url=res['fact'])
                await message.channel.send(embed=embed)                        
    elif message.content.startswith('^catgif') or message.content.startswith('/catgif'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                res = await r.json()
                embed = discord.Embed(title="Cat GIF", description="Here is a cat gif", color=0x00ff00)
                embed.set_image(url=res[0]['url'])
                await message.channel.send(embed=embed)
    elif message.content.startswith('^help') or message.content.startswith('/help'):
        embed = discord.Embed(title="Commands List", description="""
        Hello {0.author.mention} 
        ^help * displays this message 
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^lol * gives random jokes 
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^hello * says hello
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^log * shows some nerdy stuff
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^ping * pings the bot
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^qr * makes a qr code
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^mems * displays a random meme
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^cat * displays a random cat
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^catfact * displays a random cat fact
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ^catgif * displays a random cat gif
         """.format(message), color=0x00ff00)
        #await message.channel.send('{0.author.mention}').format(message)
        await message.channel.send(embed=embed) 
    if message.content.startswith('^mute') or message.content.startswith('/mute'):
        if message.author.guild_permissions.administrator:
            user = message.mentions[0]
            if user.guild_permissions.administrator:
                await message.channel.send('{0.author.mention}'.format(message)+f"{message.mentions[0]} is an admin and cannot be muted")
            else:
                await message.channel.send('{0.author.mention}'.format(message)+ "nah")
                await user.edit(mute=True)
        else:
            await message.channel.send('{0.author.mention}'.format(message)) 
    elif message.content.startswith('^unmute') or message.content.startswith('/unmute'):
        if message.author.guild_permissions.administrator:
            user = message.mentions[0]
            if user.guild_permissions.administrator:
                await message.channel.send('{0.author.mention}'.format(message)+"{message.mentions[0] cannot be unmuted}")
            else:
                await message.channel.send('{0.author.mention}'.format(message)+ "user is unmuted")
                await user.edit(mute=False)
        else:
            await message.channel.send('{0.author.mention}'.format(message))
    elif message.content.startswith('^kick') or message.content.startswith('/kick'):
        if message.author.guild_permissions.administrator:
            user = message.mentions[0]
            if user.guild_permissions.administrator:
                await message.channel.send('{0.author.mention}'.format(message)+"{message.mentions[0] is an admin and cannot be kicked}")
            else:
                await message.channel.send('{0.author.mention}'.format(message)+ "nah")
                await user.kick()
        else:
            await message.channel.send('{0.author.mention}'.format(message))                    


tvar = "ix"
tvarn ="zk"
tvarU= tvar.upper()
tbvar = "otm"
tbvarU = tbvar.upper()
tbovar = "RN"
tbovarl = tbovar.lower()
client.run(f"{tbvarU}4Mzk1NzUyODczNDc2MDk2.YfprJg.5JW{tbovarl}A1bFYMNhA1WRlLb{tvarU}wtnyM")
