import sqlite3
from discord.ext import commands

class Stats:
    def __init__(self, statbot):
        self.statbot = statbot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()


