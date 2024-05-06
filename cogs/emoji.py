#!/usr/bin/python
# -*- coding: UTF-8 -*-

from disnake import ApplicationCommandInteraction, Option, OptionType, PartialEmoji, ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from core.bot import Bot
from core.embeds import SuccessEmbed, ErrorEmbed


class GetEmoji(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="getemoji",
        description="Just get emoji then download it.",
        options=[Option(name="emoji", description="你要抓的表情符號", type=OptionType.string, required=True)],
    )
    async def getemoji(self, interaction: ApplicationCommandInteraction, emoji: str):
        if (emoji.startswith("<:") or emoji.startswith("<a:")) and emoji.endswith(">"):
            emoji = PartialEmoji.from_str(emoji)
            real = PartialEmoji.with_state(state=self.bot._connection, name=emoji.name, animated=emoji.animated, id=emoji.id)
        
            embed = SuccessEmbed(title=real.name)
            embed.set_image(file=await real.to_file())
            
            components = [
                Button(label="下載連結", style=ButtonStyle.link, url=real.url)
            ]
            
            await interaction.response.send_message(embed=embed, components=components)
        else:
            return await interaction.response.send_message(embed=ErrorEmbed("請輸入正確的表情符號格式!"))


def setup(bot: commands.Bot):
    bot.add_cog(GetEmoji(bot))
