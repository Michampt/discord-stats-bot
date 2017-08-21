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

        if not args:
            return await self.statbot.say("```" + self.pubstats.help + "```")
        else:
            player = args[0]

        if len(args) < 3:
            return await self.statbot.say("```" + self.pubstats.help + "```")

        if args[1] not in ['solo', 'duo', 'squad']:
            return await self.statbot.say("Mode must be solo duo or squad")
        else:
            mode = args[1]

        if args[2] not in ['as', 'na', 'agg']:
            return await self.statbot.say("Region must be as, na or agg")
        else:
            region = args[2]
        try:
            stats = self.api.player_mode_stats(player, game_mode=mode, game_region=region)
            if not stats:
                return await self.statbot.say("{} user has no stats for game mode: {} in region: {}".format(player,
                                                                                                        mode,
                                                                                                        region))
            else:
                stats = stats[0]
            stats = stats["Stats"]
        except KeyError:
            return await self.statbot.say("Player not found")

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

        string = "```{} stats for {}:{}".format(mode.upper(), player.title(), "\n\n")
        for s in statlist:
            string = string + s
        string = string + "```"
        return await self.statbot.say(string)

    @commands.command(pass_context=False, help="!pubskill <name> <mode>\n\n"
                                               "Displays the players skill levels in all regions and aggregate")
    async def pubskill(self, *args):
        if not args:
            return await self.statbot.say("```" + self.pubskill.help + "```")
        else:
            player = args[0]

        if len(args) < 2:
            return await self.statbot.say("```" + self.pubskill.help + "```")

        if args[1] not in ['solo', 'duo', 'squad']:
            return await self.statbot.say("Mode must be solo duo or squad")
        else:
            mode = args[1]

        try:
            stats = self.api.player_skill(player, game_mode=mode)
            if not stats:
                return await self.statbot.say("{} has no skills recorded for {} in {}".format(player.title(), mode.upper(), region.upper()))

            s = "```{} skill levels for {}:\n\n".format(player, mode)

            if 'na' in stats:
                s = s + "NA: {}\n".format(stats["na"])

            if 'as' in stats:
                s = s + "Asia: {}\n".format(stats["as"])

            if 'agg' in stats:
                s = s + "Agg: {}\n".format(stats["agg"])

            s = s + "```"
            return await self.statbot.say(s)
        except KeyError:
            return await self.statbot.say("Player not found")


def setup(statbot):
    statbot.add_cog(Stats(statbot))
