import secrets
from discord.ext import commands
from pypubg import core


class Stats:
    def __init__(self, statbot):
        self.statbot = statbot
        self.api = core.PUBGAPI(secrets.PUBG_STATS_TOKEN)

    @commands.command(pass_context=False, help="!pubstats <name> <mode> <region>\n\n"
                                               "Displays a few stats from the chosen game mode on the chosen region\n\n"
                                               "EXAMPLE: !pubstats rauxz duo na\n\n"
                                               "na = North America\n"
                                               "as = Asia\n"
                                               "agg = Aggregate (combined)")
    async def pubstats(self, *args):

        player = args[0]
        mode = args[1]
        region = args[2]

        if args[1] not in ['solo', 'duo', 'squad']:
            return await self.statbot.say("Mode must be solo duo or squad")

        if args[2] not in ['as', 'na', 'agg']:
            return await self.statbot.say("Region must be as, na or agg")

        stats = self.api.player_mode_stats(player, game_mode=mode, game_region=region)
        if not stats:
            return await self.statbot.say("{} user has no stats for game mode: {} in region: {}".format(player,
                                                                                                        mode,
                                                                                                        region))
        else:
            stats = stats[0]
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

        string = "```{} stats for {}:{}".format(mode, player, "\n")
        for s in statlist:
            string = string + s
        string = string + "```"
        return await self.statbot.say(string)

    @commands.command(pass_context=False, help="!pubskill <name> <mode>\n\n"
                                               "Displays the players skill levels in all regions and aggregate")
    async def pubskill(self, *args):
        player = args[0]
        mode = args[1]

        if args[1] not in ['solo', 'duo', 'squad']:
            return await self.statbot.say("Mode must be solo duo or squad")

        stats = self.api.player_skill(player, game_mode=mode)
        if not stats:
            return await self.statbot.say("{} user has no skills recorded for game mode: {}".format(player, mode))

        na = stats["na"]
        asia = stats["as"]
        agg = stats["agg"]

        return await self.statbot.say("```{} skill levels are currently as follows for game mode {}:\n"
                                      "NA: {}\n"
                                      "AS: {}\n"
                                      "Aggregate: {}```".format(player, mode, na, asia, agg))


def setup(statbot):
    statbot.add_cog(Stats(statbot))
