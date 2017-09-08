import sqlite3
from discord.ext import commands


class StatbotInfo:
    def __init__(self, statbot):
        self.statbot = statbot
        self.conn = sqlite3.connect('db/statbot.db')
        self.cur = self.conn.cursor()

    @commands.command(pass_context=False, help="!statbot\n\n"
                                               "Displays information about statbot\n\n")
    async def statbotinfo(self, *args):
        self.cur.execute("SELECT VERSION FROM STATBOT;")
        version = self.cur.fetchall()
        if not version:
            return await self.statbot.say("```Version: Not Currently Set.```")
        else:
            return await self.statbot.say("```Version: {}```".format(version[0][0]))


def setup(statbot):
    statbot.add_cog(StatbotInfo(statbot))
