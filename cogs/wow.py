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
        char = args[0]
        realm = args[1]

        url = "https://us.api.battle.net/{}/character/{}/{}?locale=en_US&apikey={}".format(self.game,
                                                                                           realm,
                                                                                           char,
                                                                                           self.key,)

        response = req.urlopen(url)
        character = json.loads(response.read())

        for k, v in self.races.items():
            if v == character['race']:
                race = k
                break

        for k, v in self.classes.items():
            if v == character['class']:
                char_class = k
                break

        for k, v in self.genders.items():
            if v == character['gender']:
                gender = k
                break

        for k, v in self.factions.items():
            if v == character['faction']:
                faction = k
                break

        return await self.statbot.say("```Character: {}\n"
                                      "Realm: {}\n"
                                      "Level: {}\n"
                                      "Faction: {}\n"
                                      "Gender: {}\n"
                                      "Race: {}\n"
                                      "Class: {}\n"
                                      "Total HK: {}\n"
                                      "Achievement Points: {}\n"
                                      "```".format(character['name'],
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
        char = args[0]
        realm = args[1]

        url = "https://us.api.battle.net/{}/character/{}/{}?fields=items&locale=en_US&apikey={}".format(self.game,
                                                                                                        realm,
                                                                                                        char,
                                                                                                        self.key, )

        response = req.urlopen(url)
        character = json.loads(response.read())

        s = "```Character: " + character['name'] + "\n" + "Realm: " + character['realm'] + "\n"
        s = s + "Average Item Level (Equipped): " + str(character['items']['averageItemLevelEquipped']) + "\n\n"

        try:
            head = "Head: " + character['items']['head']['name'] + " " + "(" + \
                   str(character['items']['head']['itemLevel']) + ")\n"
        except KeyError:
            head = "Head: None\n"

        try:
            neck = "Neck: " + character['items']['neck']['name'] + " " + "(" + \
                   str(character['items']['neck']['itemLevel']) + ")\n"
        except KeyError:
            neck = "Neck: None\n"

        try:
            shoulder = "Shoulder: " + character['items']['shoulder']['name'] + " " + "(" + \
                       str(character['items']['shoulder']['itemLevel']) + ")\n"
        except KeyError:
            shoulder = "Shoulder: None\n"

        try:
            back = "Back: " + character['items']['back']['name'] + " " + "(" + \
                   str(character['items']['back']['itemLevel']) + ")\n"
        except KeyError:
            back = "Back: None\n"

        try:
            chest = "Chest: " + character['items']['chest']['name'] + " " + "(" + \
                    str(character['items']['chest']['itemLevel']) + ")\n"
        except KeyError:
            chest = "Chest: None\n"

        try:
            wrist = "Wrist: " + character['items']['wrist']['name'] + " " + "(" + \
                    str(character['items']['wrist']['itemLevel']) + ")\n"
        except KeyError:
            wrist = "Wrist: None\n"

        try:
            waist = "Waist: " + character['items']['waist']['name'] + " " + "(" + \
                    str(character['items']['waist']['itemLevel']) + ")\n"
        except KeyError:
            waist = "Waist: None\n"

        try:
            legs = "Legs: " + character['items']['legs']['name'] + " " + "(" + \
                    str(character['items']['legs']['itemLevel']) + ")\n"
        except KeyError:
            legs = "Legs: None\n"

        try:
            feet = "Feet: " + character['items']['feet']['name'] + " " + "(" + \
                   str(character['items']['feet']['itemLevel']) + ")\n"
        except KeyError:
            feet = "Feet: None\n"

        try:
            finger1 = "Finger: " + character['items']['finger1']['name'] + " " + "(" + \
                      str(character['items']['finger1']['itemLevel']) + ")\n"
        except KeyError:
            finger1 = "Finger: None\n"

        try:
            finger2 = "Finger: " + character['items']['finger2']['name'] + " " + "(" + \
                      str(character['items']['finger2']['itemLevel']) + ")\n"
        except KeyError:
            finger2 = "Finger: None\n"

        try:
            trinket1 = "Trinket: " + character['items']['trinket1']['name'] + " " + "(" + \
                       str(character['items']['trinket1']['itemLevel']) + ")\n"
        except KeyError:
            trinket1 = "Trinket: None\n"

        try:
            trinket2 = "Trinket: " + character['items']['trinket2']['name'] + " " + "(" + \
                       str(character['items']['trinket2']['itemLevel']) + ")\n"
        except KeyError:
            trinket1 = "Trinket: None\n"

        try:
            mainhand = "Main Hand: " + character['items']['mainHand']['name'] + " " + "(" + \
                       str(character['items']['mainHand']['itemLevel']) + ")\n"
        except KeyError:
            mainhand = "Main Hand: None\n"

        try:
            offhand = "Off Hand: " + character['items']['offHand']['name'] + " " + "(" + \
                      str(character['items']['offHand']['itemLevel']) + ")\n"
        except KeyError:
            offhand = "Off Hand: None\n"

        s = s + head + neck + shoulder + back + chest + wrist + waist + legs + feet + finger1 + finger2 + trinket1 + \
            trinket2 + mainhand + offhand + "```"

        return await self.statbot.say(s)


def setup(statbot):
    statbot.add_cog(WowStats(statbot))
