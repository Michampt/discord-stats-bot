import secrets, pydest, sqlite3, json
from discord.ext import commands


class Destiny2:

    def __init__(self, statbot):
        self.statbot = statbot
        self.conn = sqlite3.connect('db/statbot.db')
        self.cur = self.conn.cursor()
        self.platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 4}
        self.races = {0: 'Human', 1: 'Awoken', 2: 'Exo'}
        self.classes = {0: 'Titan', 1 : 'Hunter', 2: 'Warlock', }
        self.genders = {0: 'Male', 1: 'Female'}
        self.destiny = pydest.Pydest(secrets.DESTINY2_KEY)

    @commands.command(pass_context=True, help="!register <BattleNet ID> <platform>\n"
                                              "Registering while already having an existing entry will overwrite "
                                              "the previous entry.")
    async def register(self, ctx, *args):
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

    @commands.command(pass_context=True, help="!destinycharacters <character name>")
    async def destinycharacters(self, ctx, *args):

        sender = ctx.message.author
        discord_id = sender.id
        components = ["200"]

        self.cur.execute("SELECT BUNGIE_MEMBER_ID, PLATFORM FROM DESTINY_USERS WHERE DISCORD_USER_ID=?;", (discord_id,))
        result = self.cur.fetchone()

        member_id = result[0]
        platform = result[1]

        if not result:
            return await self.statbot.say("{} You need to register your battlenet ID first using: !register.\n"
                                          + "```" + self.register.help + "```".format(sender.mention))
        else:
            response = await self.destiny.api.get_profile(platform, member_id, components)
            chars = response["Response"]["characters"]["data"]
            string = ""
            for character in chars:
                char = chars[character]
                race = char["raceType"]
                race = self.races.get(race)
                level = char["levelProgression"]["level"]
                class_type = char["classType"]
                class_type = self.classes.get(class_type)
                gender = char["genderType"]
                gender = self.genders.get(gender)
                light = char["light"]
                emblem = "https://www.bungie.net" + char["emblemPath"]
                string = string + "```Level: {}\nGender: {}\nRace: {}\nClass: {}\nLight: {}\n```".format(
                    level, gender, race, class_type, light,)

                return await self.statbot.say(string)


def setup(statbot):
    statbot.add_cog(Destiny2(statbot))
