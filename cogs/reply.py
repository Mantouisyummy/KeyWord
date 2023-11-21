from disnake import (
    ApplicationCommandInteraction,
    Option,
    OptionType,
    Message,
    OptionChoice,
    AllowedMentions,
)
from disnake.ext import commands

from core.bot import Bot
from core.embeds import SuccessEmbed, ErrorEmbed, InfoEmbed
from core.paginator import Paginator

import json
import os

# pylint: disable=C0116
# pylint: disable=C0115


class ReplySystem(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def extract_id_text(self, key: str):
        underline = key.rfind("_")
        if underline != -1:
            text = key[:underline]
            number = int(key[underline + 1 :])
            return text, number
        return key, None

    @commands.slash_command(name="回復", description="just a test")
    async def reply(self, interaction: ApplicationCommandInteraction):
        pass

    @reply.sub_command(
        name="增加",
        description="增加一個關鍵詞",
        options=[
            Option(
                name="keyword",
                description="新增觸發關鍵詞",
                type=OptionType.string,
                required=True,
            ),
            Option(
                name="reply",
                description="觸發關鍵詞後的回覆",
                type=OptionType.string,
                required=True,
            ),
        ],
    )
    async def add(
        self, interaction: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data = json.load(f)

            data[keyword + "_" + str(interaction.user.id)] = reply

            with open(
                f"./guild/{interaction.guild_id}.json", mode="w", encoding="utf-8"
            ) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with open(
                f"./guild/{interaction.guild_id}.json", mode="w", encoding="utf-8"
            ) as f:
                f.write(
                    json.dumps(
                        {keyword + "_" + str(interaction.user.id): reply},
                        ensure_ascii=False,
                        indent=4,
                    )
                )

        return await interaction.response.send_message(
            embed=SuccessEmbed(
                title="新增成功!", description=f"已新增 `{keyword}` -> `{reply}`!"
            )
        )

    @reply.sub_command(
        name="移除",
        description="移除一個關鍵詞",
        options=[
            Option(
                name="keyword",
                description="移除觸發關鍵詞",
                type=OptionType.string,
                required=True,
            ),
        ],
    )
    async def remove(self, interaction: ApplicationCommandInteraction, keyword: str):
        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)

            if interaction.user.guild_permissions.manage_messages:
                if data.get(keyword, None) is not None:
                    del data[keyword]
                    with open(
                        f"./guild/{interaction.guild_id}.json",
                        mode="w",
                        encoding="utf-8",
                    ) as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    text = self.extract_id_text(keyword)[0]
                    return await interaction.response.send_message(
                        embed=SuccessEmbed(title="移除成功!", description=f"已移除 `{text}`")
                    )
                return await interaction.response.send_message(
                    embed=ErrorEmbed(title="沒有這個關鍵詞!"), ephemeral=True
                )
            number = self.extract_id_text(keyword)[1]
            if number == interaction.user.id:
                if data.get(keyword, None) is not None:
                    del data[keyword]
                    with open(
                        f"./guild/{interaction.guild_id}.json",
                        mode="w",
                        encoding="utf-8",
                    ) as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    text = self.extract_id_text(keyword)[0]
                    return await interaction.response.send_message(
                        embed=SuccessEmbed(title="移除成功!", description=f"已移除 `{text}`")
                    )
                return await interaction.response.send_message(
                    embed=ErrorEmbed(title="沒有這個關鍵詞!"), ephemeral=True
                )
            return await interaction.response.send_message(
                embed=ErrorEmbed(title="你不能刪除別人的關鍵詞!"), ephemeral=True
            )

    @remove.autocomplete("keyword")
    async def search(self, interaction: ApplicationCommandInteraction, keyword: str):
        if not keyword:
            return []

        choices = []

        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)
            for key, value in data.items():
                text = self.extract_id_text(key)[0]
                if keyword in key:
                    choices.append(OptionChoice(name=f"{text} 回覆詞為 {value}", value=key))
            return choices
        return []

    @reply.sub_command(name="清單", description="查看已有的關鍵詞清單")
    async def replylist(self, interaction: ApplicationCommandInteraction):
        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)

            if len(data) != 0:
                pages: list[InfoEmbed] = []

                for i, (k, v) in enumerate(data.items()):
                    if i % 10 == 0:
                        pages.append(
                            InfoEmbed(
                                title="關鍵詞清單",
                                description="\n".join(
                                    [
                                        f"{i+1}. `{self.extract_id_text(key)[0]}`{f' (由 {self.bot.get_user(self.extract_id_text(key)[1]).mention} 新增)' if self.extract_id_text(key)[0] != key else ''} -> `{value}`"
                                        for key, value in list(data.items())[i : i + 10]
                                    ]
                                ),
                            )
                        )

                await Paginator(timeout=None).start(interaction, pages=pages)
            else:
                return await interaction.response.send_message(
                    embed=ErrorEmbed(title="你的群組還沒有設定過"), ephemeral=True
                )

    @reply.sub_command(
        name="變更",
        description="變更一個關鍵詞的回覆",
        options=[
            Option(
                name="keyword",
                description="觸發關鍵詞",
                type=OptionType.string,
                required=True,
            ),
            Option(
                name="reply",
                description="觸發關鍵詞後的新回覆",
                type=OptionType.string,
                required=True,
            ),
        ],
    )
    async def modify(
        self, interaction: ApplicationCommandInteraction, keyword: str, reply: str
    ):
        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)

            if interaction.user.guild_permissions.manage_messages:
                if data.get(keyword, None) is not None:
                    data[keyword] = reply
                    with open(
                        f"./guild/{interaction.guild_id}.json",
                        mode="w",
                        encoding="utf-8",
                    ) as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    text = self.extract_id_text(keyword)[0]
                    return await interaction.response.send_message(
                        embed=SuccessEmbed(
                            title="變更成功!", description=f"已變更 `{text}` 回復詞為 {reply}"
                        )
                    )
                return await interaction.response.send_message(
                    embed=ErrorEmbed(title="沒有這個關鍵詞!"), ephemeral=True
                )
            number = self.extract_id_text(keyword)[1]
            if number == interaction.user.id:
                if data.get(keyword, None) is not None:
                    del data[keyword]
                    with open(
                        f"./guild/{interaction.guild_id}.json",
                        mode="w",
                        encoding="utf-8",
                    ) as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    text = self.extract_id_text(keyword)[0]
                    return await interaction.response.send_message(
                        embed=SuccessEmbed(
                            title="變更成功!", description=f"已變更 `{text}` 回復詞為 {reply}"
                        )
                    )
                return await interaction.response.send_message(
                    embed=ErrorEmbed(title="沒有這個關鍵詞!"), ephemeral=True
                )
            return await interaction.response.send_message(
                embed=ErrorEmbed(title="你不能變更別人的關鍵詞!"), ephemeral=True
            )

    @modify.autocomplete("keyword")
    async def modify_search(self, interaction: ApplicationCommandInteraction, keyword: str):
        choices = []
        if not keyword:
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)
            for key, value in data.items():
                text = self.extract_id_text(key)[0]
                if keyword in key:
                    choices.append(OptionChoice(name=f"{text} 回覆詞為 {value}", value=key))
            return choices

        if os.path.isfile(f"./guild/{interaction.guild_id}.json"):
            with open(
                f"./guild/{interaction.guild_id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)
            for key, value in data.items():
                text = self.extract_id_text(key)[0]
                if keyword in key:
                    choices.append(OptionChoice(name=f"{text} 回覆詞為 {value}", value=key))
            return choices
        return []

    @commands.Cog.listener(name="on_slash_command_error")
    async def on_slash_command_error(
        self, interaction: ApplicationCommandInteraction, error
    ):
        return await interaction.response.send_message(
            embed=ErrorEmbed(title="喔不，出現了個錯誤：(", description=f"```{error}```")
        )

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if os.path.isfile(f"./guild/{message.guild.id}.json"):
            with open(
                f"./guild/{message.guild.id}.json", mode="r", encoding="utf-8"
            ) as f:
                data: dict = json.load(f)

            for key, value in data.items():
                text = self.extract_id_text(key)[0]
                if message.content.upper() == text.upper():
                    await message.channel.send(
                        value, allowed_mentions=AllowedMentions.none()
                    )
        else:
            return


def setup(bot: commands.Bot):
    bot.add_cog(ReplySystem(bot))
