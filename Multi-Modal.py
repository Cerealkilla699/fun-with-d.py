import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="^", intents=discord.Intents.all())
    
@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("commands have been synced")

@bot.tree.command()
async def test(interaction: discord.Interaction):
    embed = discord.Embed(
        title= 'Please fill out and submit both forms',
        description= 'This application will be sent somewhere'
        )
    await interaction.response.send_message(embed = embed, view = testview(interaction))

class testview(discord.ui.View):
    def __init__(self, og_int:discord.Interaction):
        super().__init__(timeout = 600)
        self.inter=og_int
        self.dict = {}
        
    async def interaction_check(self, interaction):
        if interaction.user != self.inter.user:
            await interaction.channel.send(f'{interaction.user.mention} this application isnt for you!')
        else:
            return True
        
    @discord.ui.button(style = discord.ButtonStyle.blurple, row=1, label = 'Button 1')
    async def btn1(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(testmodal(self.dict, self.inter))
        self.btn1.disabled = True
        await self.inter.edit_original_response(view = self)
        if self.btn1.disabled and self.btn2.disabled:
            self.stop()

    @discord.ui.button(style = discord.ButtonStyle.blurple, row=2, label = 'Button 2')
    async def btn2(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(testmodal2(self.dict, self.inter))
        self.btn2.disabled = True
        await self.inter.edit_original_response(view = self)
        if self.btn1.disabled and self.btn2.disabled:
            self.stop()

class testmodal(discord.ui.Modal, title = 'Test 1'):
    def __init__(self, ansdict:dict, og_inter:discord.Interaction):
        super().__init__()
        self.ansdict = ansdict
        self.inter = og_inter

    q1 = discord.ui.TextInput(
        label = 'This is question 1'
    )
    q2 = discord.ui.TextInput(
        label = 'This is question 2'
    )
    q3 = discord.ui.TextInput(
        label = 'This is question 3'
    )
    q4 = discord.ui.TextInput(
        label = 'This is question 4'
    )
    q5 = discord.ui.TextInput(
        label = 'This is question 5'
    )

    async def on_submit(self, interaction:discord.Interaction):
        await interaction.response.send_message(content= 'Part 1 has been submitted', ephemeral= True)
        self.ansdict.update({
            self.q1.label : self.q1.value,
            self.q2.label : self.q2.value,
            self.q3.label : self.q3.value,
            self.q4.label : self.q4.value,
            self.q5.label : self.q5.value
        })
        if len(self.ansdict) == 6:
            await send_answers.sendit(self.ansdict, self.inter)

class testmodal2(discord.ui.Modal, title = 'Test 1'):
    def __init__(self, ansdict:dict, og_inter:discord.Interaction):
        super().__init__()
        self.ansdict = ansdict
        self.inter = og_inter
    q6 = discord.ui.TextInput(
        label = 'This is question 6'
    )
    async def on_submit(self, interaction:discord.Interaction):
        await interaction.response.send_message(content= 'Part 2 has been submitted', ephemeral= True)
        self.ansdict.update({
            self.q6.label : self.q6.value
        })
        if len(self.ansdict) == 6:
            await send_answers.sendit(self.ansdict, self.inter)

class send_answers():
    async def sendit(ansdict, inter):
        embed = discord.Embed(
            title = 'Here are the answers!',
            color = inter.user.color)
        for k, v in ansdict.items():
            embed.add_field(name=k, value=v, inline = False)
        embed.set_author(name=inter.user.display_name, icon_url=inter.user.display_avatar.url, url=f'http://discord.com/users/{inter.user.id}')
        channel = bot.get_channel(CHANNEL_ID_HERE)
        await channel.send(embed=embed)

bot.run(token = TOKEN)
