import json
import os
import os.path
import re
import threading
from datetime import datetime

import requests

from uptime import BotServer
import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from googleapiclient.discovery import build
from duckduckgo_search import ddg

my_api_key = "google custom search api key"
my_cse_id = "google custom search cse id"

token2 = os.environ['token'] = "token"

token = os.environ['token']

intents = discord.Intents().all()

client = commands.Bot(command_prefix=",", intents=intents)

client.remove_command('help')

status = cycle(["created by siroo2137", "thx for using <3", ",help for available commands!"])

version = "1.2"


def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	return res


@tasks.loop(seconds=60)
async def status_change():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))


@client.event
async def on_ready():
	print('ModFinder zostal uruchomiony, nick discord: {}'.format(client.user))
	status_change.start()


@client.command(aliases=['help'])
async def pomoc(ctx):
	embed = discord.Embed(title="Komendy:")
	embed.add_field(name=",google", value="(nazwa pliku ktorego szukasz)", inline=False)
	embed.add_field(name=",duckduckgo", value="(nazwa pliku ktorego szukasz)", inline=False)
	embed.add_field(name=",yandex", value="(nazwa pliku ktorego szukasz)", inline=False)
	embed.add_field(name=",sharemods", value="(metoda 1/2 (2 to ta dokladniejsza))(nazwa pliku ktorego szukasz)", inline=False)
	embed.add_field(name="Inne metody szukania wkrótce", value=" ", inline=False)
	await ctx.reply(embed=embed)


@client.command()
async def sharemods(ctx, arg1, arg2):
	if arg1 == 1:
		args_parse = arg2
		exist = os.path.exists("./logs.txt")
		data = datetime.now()
		if exist:
			with open("logs.txt", "a") as f1:
				f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
					ctx.message.author.id, args_parse, data))
		else:
			with open("logs.txt", "w") as f1:
				f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
					ctx.message.author.id, args_parse, data))
		
		if ".zip" in arg2 or ".rar" in arg2 or ".scs" in arg2:
			arg2 = str(arg2).replace(".zip", "").replace(".rar", "").replace(".scs", "")
		
		result = google_search(f'site:sharemods.com {arg2}', my_api_key, my_cse_id)
		e = json.loads(json.dumps(result))
		dlugosc = e["searchInformation"]['totalResults']
		dlugosc = int(dlugosc) - 1
		if int(dlugosc) > 0:
			embed = discord.Embed(title="__**Szukanie Google**__ __**|**__ - ModFinder v{}".format(version), color=0x19cc70)
			embed.set_thumbnail(url="https://sharemods.com/favicon.ico")
			for _ in range(int(dlugosc)):
				embed.add_field(name="**Nazwa:** ", value="```{}```".format(e["items"][_]["title"]), inline=False)
				embed.add_field(name="**Link:** ", value="[**Link**]({})".format(e["items"][_]["link"]), inline=False)
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("✅")
			embed.add_field(name="**Ilosc wynikow:** {}".format(dlugosc), value=" ", inline=False)
			embed.set_footer(text='created by siroo2137 aka system.out.println("elo benc")#8437')
			await ctx.reply(embed=embed)
		else:
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("❌")
			await ctx.reply("Nic nie znaleziono!")
	elif arg1 == 2:
		id_msg = await ctx.fetch_message(ctx.message.id)
		await id_msg.add_reaction("✅")
		exist = os.path.exists("./logs.txt")
		data = datetime.now()
		if exist:
			f1 = open("logs.txt", "a")
			f1.write("{'user': '" + str(ctx.message.author.id) + "', 'phrase':'" + str(arg2) + "', 'date':'" + str(
				data) + "'}\n")
			f1.close()
		else:
			f1 = open("logs.txt", "w")
			f1.write("{'user': '" + str(ctx.message.author.id) + "', 'phrase':'" + str(arg2) + "', 'date':'" + str(
				data) + "'}\n")
			f1.close()
		
		try:
			r2 = requests.get("https://sharemods.com/sitemap.txt")
			with open('temp.txt', 'w', encoding="utf-8") as f1:
				f1.write(r2.text)
		except ConnectionError:
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("❌")
			await ctx.reply("Nie udalo sie polaczyc z listą linków!")
		
		with open('temp.txt', 'r', encoding='utf-8') as f:
			tomaz = f.read()
		
		match = re.search(r"https://sharemods\.com/[\w/]+/(?P<part>{}).*".format(str(arg2)), tomaz, re.MULTILINE)
		if match:
			linijka = match.group()
			linijka2 = re.search("/([^/]+\.html)$", linijka)
			nazwa = linijka2.group(1).replace(".html", "")
			embed = discord.Embed(title="__**Szukanie ShareMods**__ __**|**__ - ModFinder v{}".format(version), color=0x19cc70)
			embed.set_thumbnail(url="https://sharemods.com/favicon.ico")
			embed.add_field(name="**Nazwa:** ", value="```{}```".format(nazwa), inline=False)
			embed.add_field(name="**Link:** ", value="[**Link**]({})".format(linijka), inline=False)
			embed.set_footer(text='created by siroo2137 aka system.out.println("elo benc")#8437')
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("✅")
			await ctx.reply(embed=embed)
		else:
			embed = discord.Embed(title=" ", description=" ")
			embed.set_author(name="Taki plik nie został znaleziony na sharemods!")
			await ctx.reply(embed=embed)
	else:
		id_msg = await ctx.fetch_message(ctx.message.id)
		await id_msg.add_reaction("✅")
		exist = os.path.exists("./logs.txt")
		data = datetime.now()
		if exist:
			f1 = open("logs.txt", "a")
			f1.write("{'user': '" + str(ctx.message.author.id) + "', 'phrase':'" + str(arg2) + "', 'date':'" + str(
				data) + "'}\n")
			f1.close()
		else:
			f1 = open("logs.txt", "w")
			f1.write("{'user': '" + str(ctx.message.author.id) + "', 'phrase':'" + str(arg2) + "', 'date':'" + str(
				data) + "'}\n")
			f1.close()
		
		try:
			r2 = requests.get("https://sharemods.com/sitemap.txt")
			with open('temp.txt', 'w', encoding="utf-8") as f1:
				f1.write(r2.text)
		except ConnectionError:
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("❌")
			await ctx.reply("Nie udalo sie polaczyc z listą linków!")
		
		with open('temp.txt', 'r', encoding='utf-8') as f:
			tomaz = f.read()
		
		match = re.search(r"https://sharemods\.com/[\w/]+/(?P<part>{}).*".format(str(arg2)), tomaz, re.MULTILINE)
		if match:
			linijka = match.group()
			linijka2 = re.search("/([^/]+\.html)$", linijka)
			nazwa = linijka2.group(1).replace(".html", "")
			embed = discord.Embed(title="__**Szukanie ShareMods**__ __**|**__ - ModFinder v{}".format(version), color=0x19cc70)
			embed.set_thumbnail(url="https://sharemods.com/favicon.ico")
			embed.add_field(name="**Nazwa:** ", value="```{}```".format(nazwa), inline=False)
			embed.add_field(name="**Link:** ", value="[**Link**]({})".format(linijka), inline=False)
			embed.set_footer(text='created by siroo2137 aka system.out.println("elo benc")#8437')
			id_msg = await ctx.fetch_message(ctx.message.id)
			await id_msg.add_reaction("✅")
			await ctx.reply(embed=embed)
		else:
			embed = discord.Embed(title=" ", description=" ")
			embed.set_author(name="Taki plik nie został znaleziony na sharemods!")
			await ctx.reply(embed=embed)


@client.command()
async def google(ctx, *args):
	args_parse = " ".join(args)
	exist = os.path.exists("./logs.txt")
	data = datetime.now()
	if exist:
		with open("logs.txt", "a") as f1:
			f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
				ctx.message.author.id, args_parse, data))
	else:
		with open("logs.txt", "w") as f1:
			f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
				ctx.message.author.id, args_parse, data))
	
	if ".zip" in args or ".rar" in args or ".scs" in args:
		args = str(args).replace(".zip", "").replace(".rar", "").replace(".scs", "")
	
	result = google_search(f'{args}', my_api_key, my_cse_id)
	e = json.loads(json.dumps(result))
	dlugosc = e["searchInformation"]['totalResults']
	dlugosc = int(dlugosc) - 1
	if int(dlugosc) > 0:
		embed = discord.Embed(title="__**Szukanie Google**__ __**|**__ - ModFinder v{}".format(version), color=0x19cc70)
		embed.set_thumbnail(url="https://sharemods.com/favicon.ico")
		for _ in range(int(dlugosc)):
			embed.add_field(name="**Nazwa:** ", value="```{}```".format(e["items"][_]["title"]), inline=False)
			embed.add_field(name="**Link:** ", value="[**Link**]({})".format(e["items"][_]["link"]), inline=False)
		id_msg = await ctx.fetch_message(ctx.message.id)
		await id_msg.add_reaction("✅")
		embed.add_field(name="**Ilosc wynikow:** {}".format(dlugosc), value=" ", inline=False)
		embed.set_footer(text='created by siroo2137 aka system.out.println("elo benc")#8437')
		await ctx.reply(embed=embed)
	else:
		id_msg = await ctx.fetch_message(ctx.message.id)
		await id_msg.add_reaction("❌")
		await ctx.reply("Nic nie znaleziono!")


@client.command()
async def duckduckgo(ctx, *args):
	args_parse = " ".join(args)
	exist = os.path.exists("./logs.txt")
	data = datetime.now()
	if exist:
		with open("logs.txt", "a") as f1:
			f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
				ctx.message.author.id, args_parse, data))
	else:
		with open("logs.txt", "w") as f1:
			f1.write("{{'user': '{}', 'phrase':'{}', 'date':'{}'}}\n".format(
				ctx.message.author.id, args_parse, data))
	
	if ".zip" in args or ".rar" in args or ".scs" in args_parse:
		newargs = args_parse.replace(".zip", "").replace(".rar", "").replace(".scs", "")
	else:
		newargs = args_parse
	
	result = ddg(newargs, region='wt-wt', safesearch='Off', time='y')
	e = json.loads(json.dumps(result))
	embed = discord.Embed(title="__**Szukanie DuckDuckGo**__ __**|**__ - ModFinder v{}".format(version), color=0x19cc70)
	embed.set_thumbnail(url="https://sharemods.com/favicon.ico")
	count = 0
	for item in e:
		count += 1
		if count <= 25:
			embed.add_field(name="**Nazwa:** ", value="```{}```".format(item["title"]), inline=False)
			embed.add_field(name="**Link:** ", value="[**Link**]({})".format(item["href"]), inline=False)
	
	embed.add_field(name="**Ilosc wynikow:** {}".format(count), value=" ", inline=False)
	embed.set_footer(text='created by siroo2137 aka system.out.println("elo benc")#8437')
	id_msg = await ctx.fetch_message(ctx.message.id)
	await id_msg.add_reaction("✅")
	await ctx.reply(embed=embed)


# else:
# 	id_msg = await ctx.fetch_message(ctx.message.id)
# 	await id_msg.add_reaction("❌")
# 	await ctx.reply("Nic nie znaleziono!")

@client.command()
async def logcheck(ctx):
	exist = os.path.exists("./logs.txt")
	if exist:
		file1 = open('logs.txt', 'r')
		Lines = file1.readlines()
		embed = discord.Embed(title="Log wyszukiwan", description=" ")
		for line in Lines:
			linijkaa = line.translate(str.maketrans('', '', '{}\':\n'))
			linijka9 = linijkaa.translate(str.maketrans('', '', 'userphrase date')).split(',')
			username = linijka9[0]
			username2 = await client.fetch_user(int(username))
			embed.add_field(name="Nick: {}".format(username2.name), value="Nazwa Pliku: {} Data: {}".format(linijka9[1], linijka9[2]), inline=False)
		id_msg = await ctx.fetch_message(ctx.message.id)
		await id_msg.add_reaction("✅")
		await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(title=" ", description=" ")
		embed.set_author(name=":x: Bot nie byl uzywany!")
		embed.add_field(name=" ", value=" ", inline=False)
		await ctx.reply(embed=embed)


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(title=" ", description=" ", color=0xf50505)
		embed.add_field(name="Blad :x: ", value="**Sprawdz ,help**", inline=False)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.CommandNotFound):
		embed = discord.Embed(title=" ", description=" ", color=0xf50505)
		embed.add_field(name="Blad :x: ", value="**Ta komenda nie istnieje**", inline=False)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=" ", description=" ", color=0xf50505)
		embed.add_field(name="Blad :x:", value="{}".format(str(error)), inline=False)
		await ctx.send(embed=embed)


def websrv():
	bot_server = BotServer()
	bot_server.run()


th = threading.Thread(target=websrv)
th.start()

client.run(token)
