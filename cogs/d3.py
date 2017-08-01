import secrets, json
from discord.ext import commands
from urllib import request as req


class D3Stats:

    game = 'd3'
    key = ""

    def __init__(self, statbot):
        self.statbot = statbot
        self.key = secrets.BATTLENET_KEY

    @commands.command(pass_context=False, help="!d3hero <battletag (e.g. rauxz-1162)> <character name>")
    async def d3hero(self, *args):

        if not args:
            return await self.statbot.say("```" + self.d3hero.help + "```")

        if len(args) < 2:
            return await self.statbot.say("```" + self.d3hero.help + "```")

        battletag = args[0]
        battletag = battletag.lower()

        char = args[1]
        char = char.lower()

        url_for_id = 'https://us.api.battle.net/d3/profile/{}/?locale=en_US&apikey={}'.format(battletag, self.key)
        response = req.urlopen(url_for_id)
        profile = json.loads(response.read())

        heroid = ""
        for hero in profile['heroes']:
            if hero['name'] == char:
                heroid = hero['id']
                break

        herourl = "https://us.api.battle.net/d3/profile/{}/hero/{}?locale=en_US&apikey={}".format(battletag,
                                                                                                  heroid,
                                                                                                  self.key)

        response = req.urlopen(herourl)
        heroprofile = json.loads(response.read())

        s = "**Name**: {}\n" \
            "**Class**: {}\n" \
            "**Level**: {}\n" \
            "**Paragon Level**: {}\n" \
            "**Elites Killed**: {}\n".format(heroprofile['name'],
                                             heroprofile['class'],
                                             heroprofile['level'],
                                             heroprofile['paragonLevel'],
                                             heroprofile['kills']['elites'])

        return await self.statbot.say(s)

    @commands.command(pass_context=False, help="!d3gear <battletag (e.g. rauxz-1162)> <character name>")
    async def d3gear(self, *args):

        if not args:
            return await self.statbot.say("```" + self.d3gear.help + "```")

        if len(args) < 2:
            return await self.statbot.say("```" + self.d3gear.help + "```")

        battletag = args[0]
        char = args[1]

        url_for_id = 'https://us.api.battle.net/d3/profile/{}/?locale=en_US&apikey={}'.format(battletag, self.key)
        response = req.urlopen(url_for_id)
        profile = json.loads(response.read())

        heroid = ""
        for hero in profile['heroes']:
            if hero['name'] == char:
                heroid = hero['id']
                break

        herourl = "https://us.api.battle.net/d3/profile/{}/hero/{}?locale=en_US&apikey={}".format(battletag,
                                                                                                  heroid,
                                                                                                  self.key)

        response = req.urlopen(herourl)
        heroprofile = json.loads(response.read())

        itemlist = heroprofile['items']

        s = "**Name**: {}\n" \
            "**Class**: {}\n" \
            "**Level**: {}\n" \
            "**Paragon Level**: {}\n\n".format(heroprofile['name'],
                                               heroprofile['class'],
                                               heroprofile['level'],
                                               heroprofile['paragonLevel'])

        for item in itemlist:
            if item in ['head', 'shoulders', 'torso', 'neck', 'bracers', 'torso', 'hands', 'waist', 'legs',
                        'leftFinger', 'rightFinger', 'mainHand', 'offHand']:
                itemcode = itemlist[item]['tooltipParams']
                itemcodeurl = "https://us.api.battle.net/d3/data/{}?locale=en_US&apikey={}".format(itemcode,
                                                                                                   self.key)
                itemresponse = req.urlopen(itemcodeurl)
                itemstats = json.loads(itemresponse.read())
                stat_string = ""

                prim = itemstats['attributes']['primary']
                #sec = itemstats['attributes']['secondary']
                #passive = itemstats['attributes']['passive']
                for stat in prim:
                    stat_string = stat_string + "\n\t" + stat['text']
                #for stat in sec:
                    #stat_string = stat_string + ", " + stat['text']
                #for stat in passive:
                    #stat_string = stat_string + ", " + stat['text']

                s = s + "**" + item.title() + "**: " + itemlist[item]['name'] + "\t" + stat_string + "\n"
        return await self.statbot.say(s)


def setup(statbot):
    statbot.add_cog(D3Stats(statbot))
