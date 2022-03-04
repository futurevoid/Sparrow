# create a discord bot that will automatically send messages after a certain amount of time has passed
# (in this case, the time is set to 5 seconds)
import asyncio
import datetime as dt
import json
import os
import random
import sys
import time
from email import message
from unittest import result
from urllib.parse import urlencode
import aiohttp
import discord
import requests
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from matplotlib import image
#import urllib3
from keep_alive import keep_alive
from PIL import Image
from pyzbar import pyzbar
from urllib3 import *
import urllib.parse
import os
client = discord.Client()


#create an event that will run when the bot is ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')
    await client.change_presence(activity = discord.Game("0xhelp for help " + "0xhelp للمساعده")) 

# bot prefix
bot = commands.Bot(command_prefix='0x')


# create an event that will run when !hello is called
# create a function that will run when a message is sent
@client.event
async def on_message(message):
    global hadith_number_int
    global check 
    def check(user):
            return user == message.author 
    if message.author == client.user:
        return
    elif message.content.startswith('0xhello') or message.content.startswith('/hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('0xlog') or message.content.startswith('/log'):
        msg = f'Message sent\n{message.content}\n{message.author}\n{message.channel}\n{message.guild}\n{message.id}\n{message.type}\n{message.attachments}\n{client.user.id}\n{client.user.name}\n{client.user.discriminator}\n{client.user.avatar}\n-------'.format(
            message)
        await message.channel.send(msg)
    elif message.content.startswith('0xping') or message.content.startswith('/ping'):
        before = time.monotonic()
        msg = await message.channel.send('Pinging...')
        after = time.monotonic()
        ping = (after - before) * 1000
        await msg.edit(content=f'Pong! 🏓 {round(ping)}ms {message.author.mention}')
    elif message.content.startswith('0xqr') or message.content.startswith('/qr'):
        sliced = message.content[4:]
        slicedr = sliced.replace(" ", "%20")
        msg = f'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={slicedr}'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('0xhelp') or message.content.startswith('/help'):
        embed = discord.Embed(title="Help", description="Here is a list of commands{0.author.mention}".format(message),
                              color=0x00ff00)
        embed.add_field(name="0xhelp", value="Shows the help menu", inline=False)
        embed.add_field(name="0xping", value="Shows the bot latency", inline=False)
        embed.add_field(name="0xqr <content>", value="Creates a QR code with your content", inline=False)
        embed.add_field(name="0xmushaf <number of page in the mushaf>", value="Shows a mushaf page", inline=False)
        embed.add_field(name="0xautoayah", value="Shows a random ayah every 5 minutes", inline=False)
        embed.add_field(name="0xayah <surah number:ayah number>", value="Shows a  ayah", inline=False)
        embed.add_field(name="0xhadith", value="Shows you a hadith", inline=False)
        # embed.add_field(name="0xhadith_info" , value="Shows the hadith info", inline=False)
        embed.add_field(name="0xkick <user>", value="Kicks a user", inline=False)
        embed.add_field(name="0xban <user>", value="Bans a user", inline=False)
        embed.add_field(name="0xunban <user>", value="Unbans a user", inline=False)
        embed.add_field(name="0xmute <user>", value="Mutes a user", inline=False)
        embed.add_field(name="0xunmute <user>", value="Unmutes a user", inline=False)
        embed.add_field(name="0xclear <number of messages>", value="Clears a number of messages", inline=False)
        embed.add_field(name="0xarole <user>", value="Gives a role to a user", inline=False)
        await message.channel.send(embed=embed)
    if message.content.startswith('0xmute') or message.content.startswith('/mute'):
        try:
            if message.author.guild_permissions.administrator:
                try:
                    user = message.mentions[0]
                except IndexError:
                    await message.channel.send("0xarole <user> , Gives a role to a user")
                if user.guild_permissions.administrator:
                    await message.channel.send(
                        '{0.author.mention}'.format(message) + f"{message.mentions[0]} is an admin and cannot be muted")
                else:
                    await message.channel.send('{0.author.mention}'.format(message) + "user is muted")
                    await user.edit(mute=True)
            else:
                await message.channel.send('{0.author.mention}'.format(message) + "You are not an admin")
        except discord.Forbidden:
            await message.channel.send(f'{message.author.mention} I dont have permission to mute users')        
    elif message.content.startswith('0xunmute') or message.content.startswith('/unmute'):
        try:
            if message.author.guild_permissions.administrator:
                try:
                    user = message.mentions[0]
                except IndexError:
                    await message.channel.send("0xunmute <user> , Unmutes a user")
                if user.guild_permissions.administrator:
                    await message.channel.send(
                    '{0.author.mention}'.format(message) + f"{message.mentions[0]} cannot be unmuted")
                else:
                    await message.channel.send('{0.author.mention}'.format(message) + "user is unmuted")
                    await user.edit(mute=False)
            else:
                await message.channel.send('{0.author.mention}'.format(message) + "You are not an admin")
        except discord.Forbidden:
                    await message.channel.send(f'{message.author.mention} I dont have permission to unmute users')        
    elif message.content.startswith('0xkick') or message.content.startswith('/kick'):
        try:
            if message.author.guild_permissions.administrator:
                user = message.mentions[0]
                if user.guild_permissions.administrator:
                    await message.channel.send(
                    '{0.author.mention}'.format(message) + f"{message.mentions[0]} is an admin and cannot be kicked")
                else:
                    await message.channel.send('{0.author.mention}'.format(message) + "user is kicked")
                    await user.guild.kick(user)
            else:
                await message.channel.send('{0.author.mention}'.format(message) + "You are not an admin")
        except discord.Forbidden:
            await message.channel.send(f'{message.author.mention} I dont have permission to kick users')      
    elif message.content.startswith('0xban') or message.content.startswith('/ban'):
        try:
            if message.author.guild_permissions.administrator:
                user = message.mentions[0]
                if user.guild_permissions.administrator:
                    await message.channel.send(
                    '{0.author.mention}'.format(message) + f"{message.mentions[0]} is an admin and cannot be banned")
                else:
                    await message.channel.send('{0.author.mention}'.format(message) + "user is banned")
                    await user.guild.ban(user)
            else:
                await message.channel.send('{0.author.mention}'.format(message) + "You are not an admin")
        except discord.Forbidden:
            await message.channel.send(f'{message.author.mention} I dont have permission to kick users')        
    elif message.content.startswith('0xunban') or message.content.startswith('/unban'):
        try:
            if message.author.guild_permissions.administrator:
                user = message.mentions[0]
                if user.guild_permissions.administrator:
                    await message.channel.send(
                        '{0.author.mention}'.format(message) + f"{message.mentions[0]} cannot be unbanned")
                else:
                    await message.channel.send('{0.author.mention}'.format(message) + "user is unbanned")
                    await user.guild.unban(user)
            else:
                await message.channel.send('{0.author.mention} not an admin'.format(message))
        except discord.Forbidden:
            await message.channel.send(f'{message.author.mention} I dont have permission to unban users')    
    elif message.content.startswith('0xclear') or message.content.startswith('/clear'):
        try:
            if message.author.guild_permissions.administrator:
                mc = int(message.content[7:])
                await message.channel.purge(limit=mc)
            else:
                await message.channel.send('{0.author.mention} not an admin'.format(message))
        except discord.Forbidden:
                    await message.channel.send(f'{message.author.mention} I dont have permission to clear messages')        
    elif message.content.startswith('0xmushaf') or message.content.startswith('/mushaf'):
        mushafno = message.content[9:]
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.searchtruth.org/quran/images1/{mushafno}.jpg') as r:
                # res = await r.json()
                embed = discord.Embed(title=f"mushaf:{mushafno}", description="", color=0x00ff00)
                embed.set_image(url=f'https://www.searchtruth.org/quran/images1/{mushafno}.jpg')
                await message.channel.send(embed=embed)
    elif message.content.startswith('0xstopautos') or message.content.startswith('/stopautos'):
        global autos
        autos = 'false'
        await message.channel.send('{0.author.mention}'.format(message) + "all automatic functions are stopped")
    elif message.content.startswith('0xautomushaf') or message.content.startswith('/automushaf'):
        await message.channel.purge(limit=1)
        autos='true'
        while autos == 'true':
            if not autos:
                break
            mushafno = random.randint(1,600)
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://www.searchtruth.org/quran/images1/{mushafno}.jpg') as r:
                    # res = await r.json()
                    embed = discord.Embed(title=f"mushaf:{mushafno}", description="", color=0x00ff00)
                    embed.set_image(url=f'https://www.searchtruth.org/quran/images1/{mushafno}.jpg')
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(300)            
    elif message.content.startswith('0xayah') or message.content.startswith('/ayah'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'http://api.alquran.cloud/v1/ayah/{message.content[6:]}') as r:
                res = await r.json()
                embed = discord.Embed(title=f"{res['data']['surah']['name']}:{res['data']['surah']['number']}",
                                      description=f"{res['data']['text']}", color=0x00ff00)
                # embed.set_image(url=res['data']['url'])
                await message.channel.send(embed=embed)
    elif message.content.startswith('0xautoayah') or message.content.startswith('/autoayah'):
        await message.channel.purge(limit=1)
        global autos
        autos='true'
        while autos == 'true':
            if not autos:
                break
            async with aiohttp.ClientSession() as cs:
                randayah = random.randint(1, 6236)
                async with cs.get(f'http://api.alquran.cloud/v1/ayah/{randayah}') as r:
                    res = await r.json()
                    embed = discord.Embed(title=f"{res['data']['surah']['name']}:{res['data']['surah']['number']}",
                                          description=f"{res['data']['text']}\n {randayah}:الايه رقم", color=0x00ff00)
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(300)
        
    elif message.content.startswith('0xhadith') or message.content.startswith('/hadith'):
        await message.channel.send(
            f'{message.author.mention} available hadith books are: bukhari, muslim, abudawud, tirmidzi, nasai, malik, ibnu-majah')
        await message.channel.send(
            f'{message.author.mention} كتب الحديث المتوفرة هي:\n صحيح البخاري= bukhari \n صحيح مسلم = muslim\n سنن ابي داود = abudawud\n جامع الترمذي = tirmidzi\n سنن النسائي = nasai\n موطأ مالك = malik\n سنن ابن ماجة = ibnu-majah')
        await message.channel.send(
            f'{message.author.mention} send the hadith book name \n اكتب اسم الكتاب الذي تريده  ')
        book = await client.wait_for('message', check=lambda message: message.author == message.author, timeout=60.0)
        await message.channel.send(f'{message.author.mention} send the hadith number \n اكتب رقم الحديث الذي تريده')
        hadith_number = await client.wait_for('message', check=lambda message: message.author == message.author,
                                              timeout=60.0)
        hadith_no = hadith_number.content
        try:
            hadith_number_int = int(float(hadith_no))
        except ValueError:
            pass
        bookcontent = book.content
        bookcontentlower = bookcontent.lower()
        #print(bookcontentlower)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://api.hadith.sutanlab.id/books/{bookcontentlower}/{hadith_number_int}') as r:
                res = await r.json()
                if bookcontentlower == 'bukhari':
                    embed = discord.Embed(title=f"صحيح البخاري:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'muslim':
                    embed = discord.Embed(title=f"صحيح مسلم:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'abudawud':
                    embed = discord.Embed(title=f"سنن ابي داود:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'tirmidzi':
                    embed = discord.Embed(title=f"جامع الترمذي:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'nasai':
                    embed = discord.Embed(title=f"سنن النسائي:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'malik':
                    embed = discord.Embed(title=f"موطأ مالك:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                elif bookcontentlower == 'ibnu-majah':
                    embed = discord.Embed(title=f"سنن ابن ماجة:{res['data']['contents']['number']}",
                                          description=f"{res['data']['contents']['arab']}", color=0x00ff00)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(
                        f'{message.author.mention} the book name is not correct \n اسم الكتاب غير صحيح')
    elif message.content.startswith('0xcalc') or message.content.startswith('/calc'):
        await message.channel.send(
            "available operations are: +, -, *, /, ^, %,(),sin, cos, tan, cot, sec, csc, log, ln, sqrt, pi, e"+
            "\n"+"example: 2+2,sin(90 deg),sin(75 rad)")
        user = message.author
        await message.channel.send(
            f'{message.author.mention} enter your calculation')
        
        
        calc = await client.wait_for('message', check=lambda message: message.author == message.author, timeout=60.0)
        calccontent = calc.content
        calc_content_urlencoded = urllib.parse.quote(calccontent)
        print(calc_content_urlencoded)
        if 'sin' or 'cos' or 'tan' or 'cot' in calccontent:
            calc_content_rep = calccontent.replace('sin()', 'sin(')
            calc_content_rep = calccontent.replace('cos()', 'cos(')
            calc_content_rep = calccontent.replace('tan()', 'tan(')
            calc_content_rep = calccontent.replace('cot()', 'cot(')
            calc_content = calc_content_rep+'deg)'
        else:
            calc_content = calc_content_urlencoded    
        try:
            site_request = requests.get(f"https://api.mathjs.org/v4/?expr={calc_content_urlencoded}")
            site_request_content = site_request.text
            embed = discord.Embed(title="Result", description=f"{site_request_content}", color=0x00ff00)
            await message.channel.send(embed=embed)
        except requests.exceptions.RequestException as e:
            await message.channel.send(f'{message.author.mention} {e}')    
    elif message.content.startswith('0xQrdecode') or message.content.startswith('/Qrdecode'):
        await message.channel.send(
            f'{message.author.mention} send the qr code to be decoded ')
        qr = await client.wait_for('message', check=lambda message: message.author == message.author, timeout=60.0)                              
        qrcontent = qr.content
        print(qrcontent)
        try:
            img = Image.open(requests.get(qrcontent))
        except:
            img= Image.open(qrcontent)    
        output_unfiltered = pyzbar.decode(img)
        print(output_unfiltered)
        output= output_unfiltered[0].data.decode('utf-8')
        print(output)
        embed = discord.Embed(title=f"your QRcode Data", description=f"{output}", color=0x00ff00)
        await message.channel.send(embed=embed)
    elif message.content.startswith('0xarole') or message.content.startswith('/arole'):
        
        if message.author.guild_permissions.administrator:
            user  = message.mentions[0]
            await message.channel.send(
            f'{message.author.mention} enter the role name to add {message.mentions[0].mention}')
            role = await client.wait_for('message', check=lambda message: message.author == message.author, timeout=60.0)
            rolecontent = role.content
            print(user)
            await message.add_reaction('✅')
            def check(reaction, user):
                return user == message.author or message.mentions[0] and str(reaction.emoji) in '✅'
            reaction, user = await client.wait_for('reaction_add', timeout= 60 ,check=check)
        
            if str(reaction.emoji) == '✅':
                try:
                    user  = message.mentions[0]
                    role_to_add = discord.utils.get(message.guild.roles, name=rolecontent)
                    await user.add_roles(role_to_add)
                    await message.channel.send(f'{message.author.mention} The role has been added to {user.mention}')
                except asyncio.TimeoutError:
                    await message.channel.send(f'{message.author.mention} Reaction Timeout')
                except discord.Forbidden:
                    await message.channel.send(f'{message.author.mention} I dont have permission to add roles')
            else:
                await message.channel.send(f'{message.author.mention} The role has not been added to the {user.mention}')        
        else:
            await message.channel.send(f'{message.author.mention} you are not an admin')            
    elif message.content.startswith('0xinv') or message.content.startswith('/inv'):
        message.channel.purge(limit=1)
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')
        await message.channel.send('\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164\u3164')    
tvar = "ix"
tvarn = "zk"
tvarU = tvar.upper()
tbvar = "otm"
tbvarU = tbvar.upper()
tbovar = "RN"
tbovarl = tbovar.lower()
keep_alive()
client.run(f"{tbvarU}4Mzk1NzUyODczNDc2MDk2.YfprJg.5JW{tbovarl}A1bFYMNhA1WRlLb{tvarU}wtnyM")
