import secrets, json
from discord.ext import commands
from urllib import request as req


class WowStats:
    races = {'Human': 1,
             'Orc': 2,
             'Dwarf': 3,
             'Night Elf': 4,
             'Undead': 5,
             'Tauren': 6,
             'Gnome': 7,
             'Troll': 8,
             'Goblin': 9,
             'Blood Elf': 10,
             'Worgen': 22,
             'Panda-a': 25,
             'Panda-h': 26,
             'Panda-n': 24}

    classes = {'Warrior': 1,
               'Paladin': 2,
               'Hunter': 3,
               'Rogue': 4,
               'Priest': 5,
               'Death Knight': 6,
               'Shaman': 7,
               'Mage': 8,
               'Warlock': 9,
               'Monk': 10,
               'Druid': 11,
               'Demon Hunter': 12}

    factions = {'Horde': 1,
               'Alliance': 2,
               'Neutral': 3}

    genders = {'Male': 0,
              'Female': 1}

    def __init__(self, statbot):
        self.statbot = statbot
        self.key = secrets.BATTLENET_KEY
        self.game = 'wow'

    @commands.command(pass_context=False, help="!wowchar <name> <realm>")
    async def wowchar(self, *args):

        if not args:
            return await self.statbot.say("'''" + self.wowchar.help + "```")

        if len(args) < 2:
            return await self.statbot.say("'''" + self.wowchar.help + "'''")

        char = args[0]
        char = char.lower()

        realm = args[1]
        realm = realm.lower()

        url = "https://us.api.battle.net/{}/character/{}/{}?locale=en_US&apikey={}".format(self.game,
                                                                                           realm,
                                                                                           char,
                                                                                           self.key,)

        response = req.urlopen(url)
        character = json.loads(response.read())

        race = ""
        for k, v in self.races.items():
            if v == character['race']:
                race = k
                break

        char_class = ""
        for k, v in self.classes.items():
            if v == character['class']:
                char_class = k
                break

        gender = ""
        for k, v in self.genders.items():
            if v == character['gender']:
                gender = k
                break

        faction = ""
        for k, v in self.factions.items():
            if v == character['faction']:
                faction = k
                break

        return await self.statbot.say("**Character**: {}\n"
                                      "**Realm**: {}\n"
                                      "**Level**: {}\n"
                                      "**Faction**: {}\n"
                                      "**Gender**: {}\n"
                                      "**Race**: {}\n"
                                      "**Class**: {}\n"
                                      "**Total HK**: {}\n"
                                      "**Achievement Points**: {}\n".format(character['name'],
                                                                            character['realm'],
                                                                            character['level'],
                                                                            faction,
                                                                            gender,
                                                                            race,
                                                                            char_class,
                                                                            character['totalHonorableKills'],
                                                                            character['achievementPoints']))

    @commands.command(pass_context=False, help="!wowgear <name> <realm>")
    async def wowgear(self, *args):

        if not args:
            return await self.statbot.say("```" + self.wowgear.help + "```")

        if len(args) < 2:
            return await self.statbot.say("```" + self.wowgear.help + "```")

        char = args[0]
        char = char.lower()

        realm = args[1]
        realm = realm.lower()

        url = "https://us.api.battle.net/{}/character/{}/{}?fields=items&locale=en_US&apikey={}".format(self.game,
                                                                                                        realm,
                                                                                                        char,
                                                                                                        self.key, )

        response = req.urlopen(url)
        character = json.loads(response.read())

        s = "**Character**: " + character['name'] + "\n" + "**Realm**: " + character['realm'] + "\n"
        s = s + "**Average Item Level (Equipped)**: " + str(character['items']['averageItemLevelEquipped']) + "\n\n"

        for itemtype in character['items']:
            if itemtype in ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'waist', 'legs', 'feet', 'finger1',
                            'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']:
                try:
                    item = character['items'][itemtype]
                    s = s + "**" + itemtype.title() + "**: " + item['name'] + " (" + str(item['itemLevel']) + ")\n"
                except KeyError:
                    s = s + "**" + itemtype.title() + "**:\n"

        return await self.statbot.say(s)


def setup(statbot):
    statbot.add_cog(WowStats(statbot))

