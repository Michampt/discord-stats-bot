import secrets
from discord.ext import commands
from pypubg import core


class Stats:
    def __init__(self, statbot):
        self.statbot = statbot
        self.api = core.PUBGAPI(secrets.PUBG_STATS_TOKEN)

    @commands.command(pass_context=False, help="!pubstats <name> <mode> <region> (e.g. !pubstats rauxz duo na)")
    async def pubstats(self, *args):

        if args[1] not in ['solo', 'duo', 'squad']:
            return await self.statbot.say("Mode must be solo duo or squad")

        if args[2] not in ['as', 'na', 'agg']:
            return await self.statbot.say("Region must be as, na or agg")

        stats = self.api.player_mode_stats(args[0], game_mode=args[1], game_region=args[2])[0]
        stats = stats["Stats"]

        statlist = []

        for stat in stats:
            if stat["label"] in ["K/D Ratio",
                                 "Win %",
                                 "Wins",
                                 "Top 10s",
                                 "Losses",
                                 "Kills",
                                 "Assists",
                                 "Suicides",
                                 "Team Kills",
                                 "Headshot Kills",
                                 "Road Kills",
                                 "Round Most Kills",
                                 "Longest Kill",
                                 "Heals",
                                 "Revives",
                                 "Knock Outs"]:
                statlist.append(stat["label"] + ": " + stat["value"] + "\n")

        string = "{} stats for {}:{}".format(args[1], args[0], "\n")
        for s in statlist:
            string = string + s
        return await self.statbot.say(string)





def setup(statbot):
    statbot.add_cog(Stats(statbot))
