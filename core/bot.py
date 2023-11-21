from logging import Logger

from disnake.ext.commands import Bot as OriginalBot



class Bot(OriginalBot):
    def __init__(self, logger: Logger, **kwargs):
        super().__init__(**kwargs)

        self.logger = logger
       
    async def on_ready(self):
        self.logger.info("The bot is ready! Logged in as %s" % self.user)

