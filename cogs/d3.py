import secrets
from discord.ext import commands


class D3Stats:

    game = 'd3'
    key = ""

    def __init__(self, statbot):
        self.statbot = statbot
        self.key = secrets.BATTLENET_KEY

    @commands.command(pass_context=False, help="!d3char <name> realm")
    async def d3char(self, *args):
        char = args[0]
        realm = args[1]

        character = "https://us.api.battle.net/{}/character/{}/{}?locale=en_US&apikey=".format(self.game,
                                                                                               self.key,
                                                                                               realm,
                                                                                               char)


def setup(statbot):
    statbot.add_cog(D3Stats(statbot))
