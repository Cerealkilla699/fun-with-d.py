import discord
from discord.ext import commands

TOKEN = (yourtokenhere)

bot = commands.Bot(command_prefix="^", intents=discord.Intents.all())

@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("commands have been synced")

class staff(discord.ui.Modal, title="Staff Application"):
#this is our first question
    age = discord.ui.TextInput(
        label = "How old are you?",
        placeholder = "Age here",
        required = True)
#second question
    tz = discord.ui.TextInput(
        label = "What timezone are you in?",
        placeholder = "EST, CST, AST",
        required = True)
    async def on_submit(self, interaction:discord.Interaction):
        embed = discord.Embed(
            title = "New Staff Application!",
            description = f"**{self.age.label}:**\n{self.age.value}\n\n**{self.tz.label}:**\n{self.tz.value}")
        embed.set_author(
            name=interaction.user.name, 
            icon_url=interaction.user.display_avatar.url, 
            url=f"http://discord.com/users/{interaction.user.id}")
        channel = bot.get_channel(YourChannelIDHere)
        newapp = await channel.send(embed = embed)
        await newapp.pin()
        await interaction.response.send_message("Your application has been submitted!", ephemeral=True)

@bot.tree.command()
async def staffapplication(interaction:discord.Interaction):
    '''Submit an application to be staff in this server'''
    await interaction.response.send_modal(staff())

bot.run(TOKEN)
