import discord
from discord import app_commands


class button_view(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout=None)
	
	@discord.ui.button(label="Akceptuje powyzszy regulamin", style=discord.ButtonStyle.gray, custom_id="role_button",
	                   emoji="<:zgoda_gray:1066112395988193350>")
	async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
		if type(client.role) is not discord.Role:
			client.role = interaction.guild.get_role(1052973544029573210)
		if client.role not in interaction.user.roles:
			await interaction.user.add_roles(client.role)
			await interaction.response.send_message("Zostales zweryfikowany!", ephemeral=True)
		else:
			await interaction.response.send_message("Jestes juz zweryfikowany!", ephemeral=True)


class aclient(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.all())
		self.synced = False
		self.added = False
		self.role = 1052973544029573210
	
	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await tree.sync(guild=discord.Object(
				id=1052220357890818158))
			self.synced = True
		if not self.added:
			self.add_view(button_view())
			self.added = True
		print(f"{self.user} wystartowal.")


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(guild=discord.Object(id=1052220357890818158), name='weryfikacja',
              description='Wysyla weryfikacje')
async def launch_button(interaction: discord.Interaction):
	embed = discord.Embed(title="**REGULAMIN SERWERA TRANS LINE**",
	                      description="\n\n**§ 1. KANAŁY TEKSTOWE:**\n\n§ 1.1 Zakaz prowokowania innych użytkowników w celu prowokowania kłótni\n§ 1.2 Zakaz reklamowania czegokolwiek bez wcześniejszego uzgodnienia tego z zarządem\n§ 1.3 Zakaz wykorzystywania błędów serwera w własnych celach. Należy takowe zgłosić.\n§ 1.4 Zakaz obrażania, wyśmiewania innych użytkowników discorda lub zarządu.\n§ 1.5 Zakaz nadużywania CAPS’a.\n§ 1.6 Zakaz Trollowania.\n§ 1.7 Zakaz się prób wyłudzenia informacji, włamania na konto oraz wszelkich innych metod wyłudzania własności.\n§ 1.8 Zakaz Żebrania.\n§ 1.9 Zakaz podszywania się pod innych użytkowników.\n§ 1.10 Zakaz udostępniania prywatnych Wiadomości, rozmów na kanałach publicznych bądz głosowych.\n§ 1.11 Zakaz udostępniania rozmów prowadzonych na kanale głosowym.\n§ 1.12 Zakaz szantażowania, grożenia innym osobą.\n§ 1.13 Zakaz Floodowania.\n§ 1.14 Zakaz wysyłania wiadomości zawierających tzw „można mod na..”.\n§ 1.15 Komendy używamy tylko na kanale do tego przystosowanym czyli #「📄」czat.\n§ 1.16 Administracja nie ponosi odpowiedzialności za treści umieszczane przez użytkowników.\n\n**§ 2. KANAŁY GŁOSOWE:**\n\n§ 2.1 Zasady obowiązujące na kanałach tekstowych, obowiązują na kanałach głosowych.\n§ 2.3 Zakaz przekrzykiwania się, specjalnego zagłuszania innych rozmówców.\n§ 2.4 Zakaz używania modulatora głosu, i innych programów do trollingu.\n§ 2.5 Zakaz nagrywania i udostępniania rozmów z kanałów głosowych bez wcześniejszego powiadomienia o tym osób uczestniczących w rozmowie.\n§ 2.6 Zakaz Krzyczenia, piszczenia, specjalnych przesterów na kanale głosowym.\n§ 2.7 Zakaz obrażania użytkowników.\n§ 2.8 Zakaz skakania po kanałach głosowych.\n§ 2.9 Wszelkie problemy z mikrofonem, typu szum bądź przegłos należy natychmiastowo naprawić.",
	                      color=0xffffff)
	embed.set_thumbnail(
		url="https://cdn.discordapp.com/attachments/938104226364665947/1066106042238386247/1784_WapisGroup_55c21d39ea867-removebg-preview.png")
	await interaction.response.send_message(embed=embed, view=button_view())


client.run("token")
