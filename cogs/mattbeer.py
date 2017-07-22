import sqlite3
from discord.ext import commands


class Stats:
    def __init__(self, statbot):
        self.statbot = statbot
        self.conn = sqlite3.connect('db/statbot.db')
        self.cur = self.conn.cursor()

    @commands.command(pass_context=True, help="!beers\n\n"
                                              "Displays the amount of total beers logged.")
    async def beers(self, ctx):
        user = ctx.message.author
        self.cur.execute("SELECT total_beers FROM beers WHERE username = ?;", (user.id,))
        total_beers = self.cur.fetchone()

        if total_beers is None:
            return await self.statbot.say("```You have yet to register any beers.```")
        if total_beers[0] == 1:
            return await self.statbot.say("```Just 1...``` https://media.giphy.com/media/xTkcEQhPwfXLCfTGQ8/giphy.gif")
        else:
            return await self.statbot.say("```So far you've downed a total of " + str(total_beers[0]) + " beers.```")

    @commands.command(pass_context=True, help="!addbeer\n\n"
                                              "Adds one beer to todays and total beers logged.")
    async def addbeer(self, ctx):
        user = ctx.message.author
        self.cur.execute("SELECT total_beers FROM beers WHERE username = ?;", (user.id,))
        total_beers = self.cur.fetchone()

        if total_beers:
            self.cur.execute("UPDATE beers SET total_beers = total_beers + 1 WHERE username = ?", (user.id,))
            self.conn.commit()
        else:
            self.cur.execute("INSERT INTO beers (username, total_beers, todays_beers) VALUES "
                             "(?, 'total_beers' + 1, ?);",
                             (user.id, 0,))
            self.conn.commit()

        self.cur.execute("SELECT total_beers FROM beers WHERE username = ?;", (user.id,))
        total_beers = self.cur.fetchone()

        return await self.statbot.say("```Your beer has been added to your count. You're currently on beer " +
                                      str(total_beers[0]) + ".```")


def setup(statbot):
    statbot.add_cog(Stats(statbot))
