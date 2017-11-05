# discord-pubg-stats-bot
Discord bot for various game stats

Python 3.6 required (Provided in the python docker image)

## modules needed:
* discord
* pypubg (provided)
* json

## keys needed
* battlenet (https://dev.battle.net/)
* pubgtracker (https://pubgtracker.com/site-api)
* discord (https://discordapp.com/developers/applications/me)
* bungie (https://destinydevs.github.io/BungieNetPlatform/docs/API-Key)

Just replace your tokens in secrets.py
* BOT_TOKEN = discord bot token
* PUBG_STATS_TOKEN = pubgtracker token
* BATTLENET_KEY = battlenet api key
* DESTINY2_KEY = api key for bungie

## Creating a Docker image:
* edit secrets.py with your keys
* run ```docker build --tag statsbot .```
* run the container with ```docker run -d statsbot:latest```

## Current bot commands
//TODO Cleanup the commands and add them here
