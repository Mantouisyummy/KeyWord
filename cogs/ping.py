import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
class View(disnake.ui.View):
    def __init__(self):
        self.temp = 1
        super().__init__(timeout=None)

    @disnake.ui.button(label="繼續戳", style=disnake.ButtonStyle.green, emoji="<:cutefox:1033313959203323924>",custom_id="update")
    async def update(self, button: disnake.ui.Button, interaction: ApplicationCommandInteraction):
            if self.temp < 2:
                self.temp = stab
                self.temp += 1
                embed = disnake.Embed(title=":ping_pong: | Pong! {} ms".format(round(bot.latency * 1000)),description=f"我被戳了`{self.temp}`次(,,・ω・,,)",colour=disnake.Colour.random())
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                self.temp += 1
                embed = disnake.Embed(title=":ping_pong: | Pong! {} ms".format(round(bot.latency * 1000)),description=f"我被戳了`{self.temp}`次(,,・ω・,,)",colour=disnake.Colour.random())
                await interaction.response.edit_message(embed=embed, view=self)

class Ping(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        super().__init__()
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View())
        print("Ping Ready!")

    @commands.slash_command(name="ping", description="偷戳一下鰻頭(｡・ω・｡)")
    async def ping(self, interaction: ApplicationCommandInteraction):
        global bot
        global message
        global stab #戳
        stab = 1
        bot = self.bot
        embed = disnake.Embed(title=":ping_pong: | Pong! {} ms".format(round(bot.latency * 1000)),description=f"我被戳了`{stab}`次(,,・ω・,,)",colour=disnake.Colour.random())
        view = View() 
        message = await interaction.response.send_message(embed=embed,view=view)

def setup(bot):
    bot.add_cog(Ping(bot))