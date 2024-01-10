from itertools import cycle

import discord
from discord.ext import commands
from discord.ext import tasks

token = "token"

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)

lista_napisow = []

with open("napisy.txt", "r") as file:
	lines = file.readlines()
	napiscount = 0
	for line in lines:
		napiscount += 1
		lista_napisow.append(line)

status = cycle(lista_napisow)


@tasks.loop(seconds=10)
async def logo():
	await bot.change_presence(
		status=discord.Status.dnd, activity=discord.Game(next(status))
	)


@bot.command
async def dodaj_napis(ctx, arg1):
	await ctx.reply("Napis || {} || dodany".format(arg1))


@bot.event
async def on_ready():
	print(
		f"{bot.user} wystartowal | Info -> ID: {bot.user.id}, ilosc statusow: {str(napiscount)}"
	)
	logo.start()


@bot.event
async def on_message(message):
	content = message.content
	if "huj" in content.lower():
		await message.reply("ci w dupe")
	elif "hój" in content.lower():
		await message.reply("ci w dupe")
	elif "hu j" in content.lower():
		await message.reply("ci w dupe")
	elif "h uj" in content.lower():
		await message.reply("ci w dupe")
	elif "hu-j" in content.lower():
		await message.reply("ci w dupe")
	elif "h-uj" in content.lower():
		await message.reply("ci w dupe")
	elif "hÓ j" in content.lower():
		await message.reply("ci w dupe")
	elif "h Ój" in content.lower():
		await message.reply("ci w dupe")
	elif "hÓ-j" in content.lower():
		await message.reply("ci w dupe")
	elif "h-Ój" in content.lower():
		await message.reply("ci w dupe")
	elif "huj" in content.lower():
		await message.reply("ci w dupe")


bot.run(token)
