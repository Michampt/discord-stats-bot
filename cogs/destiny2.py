import secrets, pydest, sqlite3
from discord.ext import commands


class Destiny2:

    def __init__(self, statbot):
        self.statbot = statbot
        self.conn = sqlite3.connect('db/statbot.db')
        self.cur = self.conn.cursor()
        self.platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 4}
        self.destiny = pydest.Pydest(secrets.DESTINY2_KEY)

    @commands.command(pass_context=True, help="!register <BattleNet ID> <platform>\n"
                                              "Registering while already having an existing entry will overwrite "
                                              "the previous entry.")
    async def register(self, ctx, *args):
        if not args:
            return await self.statbot.say("```" + self.register.help + "```")
        if len(args) < 2:
            return await self.statbot.say("```" + self.register.help + "```")

        bnet_id = args[0]
        bnet_id_web = bnet_id.replace("#", "%23")
        platform = self.platforms.get(args[1].upper())
        result = await self.destiny.api.search_destiny_player(platform, bnet_id_web)
        member_id = result['Response'][0]['membershipId']
        sender = ctx.message.author
        if result['ErrorCode'] == 1 and len(result['Response']) > 0:
            self.cur.execute("REPLACE INTO DESTINY_USERS "
                             "(DISCORD_USER_ID, BATTLE_NET_ID, BUNGIE_MEMBER_ID, PLATFORM)"
                             "values (?, ?, ?, ?);", (sender.id, bnet_id, member_id, platform))
            self.conn.commit()
            return await self.statbot.say(
                sender.mention + " You have successfully registered using {} on {}".format(
                    bnet_id, args[1]))
        else:
            return await self.statbot.say("{} Unfortunately I could not retrieve your member ID from Bungie.\n"
                                          "Please ensure you have submitted the correct "
                                          "BattleNet tag and platform".format(
                                            sender.mention, bnet_id, platform))

    @commands.command(pass_context=False, help="!destinystats <character name>")
    async def destinystats(self, *args):
        #TODO lookup in the db, the member ID, and go get the user's character(s).
        #TODO if the user does not have a member ID registered, tell them to register it.

        return await self.statbot.say()


def setup(statbot):
    statbot.add_cog(Destiny2(statbot))
