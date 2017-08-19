# discord-pubg-stats-bot
Discord bot for various game stats
Python 3.6 required

## modules needed:
* discord
* pypubg
* json

## keys needed
* battlenet (https://dev.battle.net/)
* pubgtracker (https://pubgtracker.com/site-api)
* discord (https://discordapp.com/developers/applications/me)

Just replace your tokens in secrets.py
* BOT_TOKEN = discord bot token
* PUBG_STATS_TOKEN = pubgtracker token from https://pubgtracker.com/
* BATTLENET_KEY = battlenet api key

## Creating a Docker image:
* edit secrets.py with your keys
* run ```bash docker build --tag statsbot .```
* run the container with ```bash docker run statsbot:latest```

The mattbeer module is just a joke, you don't need it.
