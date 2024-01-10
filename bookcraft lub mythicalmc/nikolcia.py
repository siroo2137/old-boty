import datetime
import discord
from discord import app_commands
from discord.ext import tasks, commands
import requests
import json

guild_id = # id serwera
general_id = # id głównego chatu
wrota_id = # id kanału na który wysłać powiadomienia o dołączeniu do serwera
drzwi_id = # id kanału na który wysłać powiadomienia o wyjściu do serwera
nowy_id = # id kanału nowy (gdy ktoś dołączy, ustawia nazwe kanału na nazwę tej osoby)
owner_role = # rola właściciela/administratora bota
verification_channel = # kanał na który wysyłać embed z weryfikacją
verified_id = # rola do nadania po weryfikacji
role_id = # rola nadana po weryfikacji (nie pamiętam różnicy pomiędzy tym a verified_id)
api_key = # klucz do api openai (chatgpt)
url = "https://api.openai.com/v1/chat/completions" # link do api do openai (chatgpt)

headers = {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer "+api_key
}

bot = commands.Bot(command_prefix="nikolcia ", intents=discord.Intents.all())

def __init__(self):
    super().__init__(intents=discord.Intents.all())
    self.synced = False
    self.added = False
    self.role = None


class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Akceptuje powyzszy regulamin",
        style=discord.ButtonStyle.gray,
        custom_id="role_button",
        emoji="<a:emoji_25:1012270304812343357>",
    )
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if bot.role is None:
            bot.role = interaction.guild.get_role(role_id)
        if bot.role not in interaction.user.roles:
            await interaction.user.add_roles(bot.role)
            await interaction.response.send_message(
                "Zostałes zweryfikowany!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Zostałeś już zweryfikowany!", ephemeral=True
            )


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    user_count_update.start()
    bot.add_view(button_view())
    print(f"{bot.user} wystartowal.")


@bot.command()
async def sendAB(ctx):
    permission_role = ctx.guild.get_role(int(owner_role))
    if permission_role in ctx.message.author.roles:
        await ctx.message.delete()
        embed = discord.Embed(title=" ")
        embed.add_field(name="❗ **Weryfikacja** ❗",
                        value="<:emoji10183:1112664647804387358> Witaj drogi użytkowniku dołączyłeś na nasze szeregi. Serwer MythicalMc.PL to serwer Minecraft oraz Discord community aby się zweryfikować to musimy upewnić się czy nie jesteś robotem więc kliknij w reakcję aby się zweryfikować. <a:zerotwo:1112663840358940702>",
                        inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1112016470164131981/1112681591181951006/sfz6myb.gif")
        message = await ctx.send(embed=embed)
        await message.add_reaction("<a:checkmark:1112663536594866196>")
    else:
        await ctx.reply("brak uprawnien cwaniaczku. :)")


async def updatecount():
    global ilosc_now
    ilosc_now = len([m for m in bot.get_guild(guild_id).members if not m.bot])


@tasks.loop(minutes=5.0, count=None)
async def user_count_update():
    await updatecount()


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != bot.user.id:
        channel = bot.get_channel(verification_channel)
        if payload.channel_id != channel.id:
            return
        guild = bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if str(payload.emoji) == "<a:checkmark:1112663536594866196>":
            role = discord.utils.get(guild.roles, id=verified_id)
            await user.remove_roles(role)
            await user.add_roles(role)

            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, user)

@bot.event
async def on_member_join(member):
    avatar = member.avatar
    await updatecount()
    channel = discord.utils.get(bot.get_guild(guild_id).channels, id=general_id)
    await channel.send(
        "Przywitajmy wszyscy __{}__ na serwerze!\n• Miłego pobytu życzy administracja serwera! <3".format(
            member.mention))
    embed = discord.Embed(title=" ",
                          description="Mamy wielką nadzieję, że zostaniesz u nas na dłuższy czas! Jeszteś naszym **{} gościem.** Dziękujemy Ci za dołączenie!".format(
                              ilosc_now),
                          color=0x11ff00)
    embed.set_author(name="Witaj {} na naszym serwerze! ".format(member.display_name), url=avatar)
    channel3 = discord.utils.get(bot.get_guild(guild_id).channels, id=wrota_id)
    await channel3.send(embed=embed)


channel4 = discord.utils.get(bot.get_guild(guild_id).channels, id=nowy_id)
await channel4.edit(name="﹝👋﹞Nowy/a: {}".format(member.name))


@bot.event
async def on_member_remove(member):
    avatar = member.avatar
    await updatecount()
    embed = discord.Embed(title=" ",
                          description="Mamy nadzieję, że jeszcze wrócisz do nas. Wierzymy w Ciebie!\nPo stracie tego członka mamy w sumie {} osób.".format(
                              ilosc_now),
                          color=0xff0000)
    embed.set_author(name="Niestety {} opuścił(a) nasz serwer!".format(member.display_name), url=avatar)
    channel3 = discord.utils.get(bot.get_guild(guild_id).channels, id=drzwi_id)
    await channel3.send(embed=embed)


@bot.event
async def on_message(message):
    if message.channel.id == 1142928664334442506 and message.author.id != bot.user.id:
        gpthistory = []
        async for newMessage in message.channel.history(limit=35):
            gpthistory.append({"role": "user", "content": newMessage.content + " *" + newMessage.author.display_name + " says.*"},)

        newGPTHistory = [
            {"role": "system", "content": "You are Nikolcia UwU, a cute anime girl.\nCarefully read what the people are saying.\nRespond using Markdown, don't include that you're saying something in your responses and be overly nice to everybody,\nBe sure to add \"~\" or \"hehe\" or \"hihi\" at the end of each message."},
        ]

        for historyMessage in gpthistory:
            newGPTHistory.append(historyMessage)

        newGPTHistory.append({"role": "user", "content": message.content + " *" + message.author.display_name + " says.*"})

        payload = {
            "model" : "gpt-3.5-turbo-16k",
            "messages" : newGPTHistory,
            "temperature" : 1,
            "top_p" : 1,
            "n" : 1,
            "stream" : False,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
        }
        response = requests.post(url, headers=headers, json=payload, stream=False)
        nikolciaResponse = json.loads(response.text)
        if "choices" in nikolciaResponse:
            formatMessage = nikolciaResponse["choices"][0]["message"]["content"].replace("*Nikolcia UwU says*", "")
            await message.reply(formatMessage)
        else:
            await message.reply("Nikolcia nie chciala odpowiedziec :(")
        return

    if message.author != bot.user:
        await bot.process_commands(message)
        if message.channel.id == 1097984514833256502:
            for member in message.mentions:
                if member.id == 388032108104384513:
                    await message.channel.send(
                        message.author.mention + ", ty kurwo jebana, ładnie to tak z właścicielem sie shipować")
                    await message.delete()
        if "DZIEŃ DOBRY".lower() == message.content.lower():
            await message.reply("hej")
        if "DO WIDZENIA".lower() == message.content.lower():
            await message.reply("paa")
        if "DOWIDZENIA".lower() == message.content.lower():
            await message.reply("paa")
        if "DO ZOBACZENIA".lower() == message.content.lower():
            await message.reply("paa")
        if "DZIEN DOBRY".lower() == message.content.lower():
            await message.reply("hej")
        if "CZEŚĆ".lower() == message.content.lower():
            await message.reply("hej")
        if "HEJ".lower() == message.content.lower():
            await message.reply("hej")
        if "NO HEJ".lower() == message.content.lower():
            await message.reply("hej")
        if "CO TAM".lower() == message.content.lower():
            await message.reply("dobrze, a co tam u ciebie?")
        if "CO TAM?".lower() == message.content.lower():
            await message.reply("dobrze, a co tam u ciebie?")
        if "JAK TAM".lower() == message.content.lower():
            await message.reply("dobrze, a co tam u ciebie?")
        if "A DOBRZE".lower() == message.content.lower():
            await message.reply("to sie ciesze <:emoji_28:1012270548333637694>")
        if "JEST".lower() == message.content.lower():
            await message.reply("to sie ciesze <:emoji_28:1012270548333637694>")
        if "DOBRANOC".lower() == message.content.lower():
            await message.reply("nawzajem <:emoji_28:1012270548333637694>")
        if "HOW ARE YOU".lower() == message.content.lower():
            await message.reply("good, how about you?")
        if "NIE LUBIE CIE".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "NIE LUBIĘ CIĘ".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "NIE LUBIĘ CIE".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "NIE LUBIE CIE NIKOLCIA".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "NIE LUBIĘ CIĘ NIKOLCIA".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "NIE LUBIĘ CIE NIKOLCIA".lower() == message.content.lower():
            await message.reply("a ja ciebie nadal lubie <:emoji_28:1012270548333637694>")
        if "HI".lower() == message.content.lower():
            await message.reply("heyy")
        if "HEY".lower() == message.content.lower():
            await message.reply("heyy")
        if "PA".lower() == message.content.lower():
            await message.reply("paa")
        if "PAPA".lower() == message.content.lower():
            await message.reply("paa")

bot.run("token")