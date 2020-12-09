import discord, discord_webhook, subprocess, sys, time, os, datetime, random, datetime, smtplib, string, itertools
import urllib.parse, urllib.request, re, json, requests, aiohttp, asyncio, colorama, PIL, io, base64, captcha

from discord.ext import (
    commands,
    tasks
)
from threading import Thread

from discord_webhook import DiscordWebhook, DiscordEmbed

import pythonping
from pythonping import ping as pinger

from itertools import cycle

loop = asyncio.get_event_loop()

intents = discord.Intents.all()

client = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True)

client.remove_command('help')

with open("config.json") as f:
    config = json.load(f)

regAPI = config.get('RegularAPIurl')
RegMethodList = config.get('RegularMethodsList')

premAPI = config.get('PremiumAPIurl')
PremMethodList = config.get('PremiumMethodsList')

token = config.get('token')

@client.event
async def on_ready():
    while True:
        await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"The War On Homes", type=5))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f">help", type=5))
        await asyncio.sleep(5)

@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.MissingRequiredArgument):
    	await ctx.send(f'{ctx.author.mention}, {error}')

@client.command()
async def help(ctx):
	embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Commands", color=0xfefefe)
	embed.add_field(name=">normal flood [ip] [port] [time] [method]", value="Sends A DDoS Attack Using Regular Network", inline=False)
	embed.add_field(name=">normal methods", value="Shows Methods For Regular Plan", inline=False)
	embed.add_field(name=">premium flood [ip] [port] [time] [method]", value="Sends DDoS Attack Using Premium Network", inline=False)
	embed.add_field(name=">nmap [ip]", value="Performs A NMAP Port Scan On Specified Host", inline=False)
	embed.add_field(name=">icmping [ip]", value="Performs A ICMP Ping With Checkhost.net", inline=False)
	embed.add_field(name=">tcpping [ip]:[port]", value="Performs A TCP Ping With Checkhost.net", inline=False)
	embed.add_field(name=">trace [ip]", value="Performs A IP Lookup On Specified Host", inline=False)
	embed.add_field(name=">ping [ip]", value="Pings Specified Host", inline=False)
	await ctx.send(embed=embed)

@client.group(invoke_without_command=True, case_insensitive=True)
async def normal(ctx):
	await ctx.send(f'{ctx.author.mention}, There are 2 commands in this category, >normal methods | >normal flood', delete_after=30)

@normal.command()
async def methods(ctx):
	embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Regular Methods -", color=0xfefefe, description=RegMethodList)
	await ctx.send(embed=embed)

@normal.command()
async def flood(ctx, ip, port, time, method):
	embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Attack Sent!", color=0xfefefe)
	embed.add_field(name="Host -", value=ip, inline=False)
	embed.add_field(name="Port -", value=port, inline=False)
	embed.add_field(name="Time -", value=time, inline=False)
	embed.add_field(name="Method -", value=method, inline=False)
	embed.add_field(name="Network -", value="Regular", inline=False)
	embed.set_footer(text=f"Attack Sent By {ctx.author}")
	await ctx.send(embed=embed)

@client.group(invoke_without_command=True, case_insensitive=True)
async def premium(ctx):
	await ctx.send(f'{ctx.author.mention}, There are 2 commands in this category, >premium methods | >premium flood', delete_after=30)

@premium.command()
async def methods(ctx):
	embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Premium Methods -", color=0xfefefe, description=PremMethodList)
	await ctx.send(embed=embed)

@premium.command()
async def flood(ctx, ip, port, time, method):
	embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Attack Sent!", color=0xfefefe)
	embed.add_field(name="Host -", value=ip, inline=False)
	embed.add_field(name="Port -", value=port, inline=False)
	embed.add_field(name="Time -", value=time, inline=False)
	embed.add_field(name="Method -", value=method, inline=False)
	embed.add_field(name="Network -", value="Premium", inline=False)
	embed.set_footer(text=f"Attack Sent By {ctx.author}")
	await ctx.send(embed=embed)


@client.command(aliases=['trace'])
async def geoip(ctx, *, ip: str = '1.1.1.1'):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=22232633') 
        geo = r.json()
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="**IP Lookup**", color=0xfefefe)
        try:
        	embed.add_field(name="IP", value=geo['query'], inline=False)
        except:
        	embed.add_field(name="IP", value="None", inline=False)
        try:
        	embed.add_field(name="City", value=geo['city'], inline=False)
        except:
        	embed.add_field(name="City", value="None", inline=False)
        try:
        	embed.add_field(name="Region/State", value=geo['regionName'], inline=False)
        except:
        	embed.add_field(name="Region/State", value="None", inline=False)
        try:
        	embed.add_field(name="Country", value=geo['country'], inline=False)
        except:
        	embed.add_field(name="Country", value="None", inline=False)
        try:
        	embed.add_field(name="Continent", value=geo['continent'], inline=False)
        except:
        	embed.add_field(name="Continent", value="None", inline=False)
        try:
        	embed.add_field(name="ISP", value=geo['isp'], inline=False)
        except:
        	embed.add_field(name="ISP", value="None", inline=False)
        try:
        	embed.add_field(name="Organization", value=geo['org'], inline=False)
        except:
        	embed.add_field(name="Organization", value="None", inline=False)
        try:
        	embed.add_field(name="Reverse DNS", value=geo['reverse'], inline=False)
        except:
        	embed.add_field(name="Reverse DNS", value="None", inline=False)
        try:
        	embed.add_field(name="AS", value=geo['as'], inline=False)
        except:
        	embed.add_field(name="AS", value="None", inline=False)
        try:
        	embed.add_field(name="Mobile?", value=geo['mobile'], inline=False)
        except:
        	embed.add_field(name="Mobile?", value="None", inline=False)
        try:
        	embed.add_field(name="Proxy/VPN?", value=geo['proxy'], inline=False)
        except:
        	embed.add_field(name="Proxy/VPN?", value="None", inline=False)
        try:
        	embed.add_field(name="Hosting?", value=geo['hosting'], inline=False)
        except:
        	embed.add_field(name="Hosting?", value="None", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
    except:
        await ctx.send('Not A Valid IP/No Info Found!', delete_after=60)

@client.command()
async def icmping(ctx, *, ip: str = '1.1.1.1'):
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(f'https://check-host.net/check-ping?host={ip}&max_nodes=15', headers=headers).text
    host = json.loads(r)
    embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="**ICMP Check Host**", color=0xfefefe)
    embed.add_field(name="Link To Report", value=host['permanent_link'], inline=False)
    await ctx.send(embed=embed)
   
@client.command()
async def tcping(ctx, *, ip: str = '1.1.1.1:443'):
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(f'https://check-host.net/check-tcp?host={ip}&max_nodes=15', headers=headers).text
    host = json.loads(r)
    embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="**TCP Check Host**", color=0xfefefe)
    embed.add_field(name="Link To Report", value=host['permanent_link'], inline=False)
    await ctx.send(embed=embed)

@client.command()
async def nmap(ctx, ip: str = '1.1.1.1'):
    if not ip:
        await ctx.send('You need to enter a IP address to scan!', delete_after=30)
    else:
        scan = requests.get(f'https://api.hackertarget.com/nmap/?q={ip}').text
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xfefefe)
        embed.add_field(name='Port Scan Results:', value=f'{scan}')
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

@client.command()
async def ping(ctx, ip: str = '1.1.1.1'):
     res = pinger(f"{ip}", count=10, timeout=.5)
     await ctx.send(res)


client.run(token)