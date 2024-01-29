""" This is a very simple script to put the FAQ bot skeleton code on line
as a discord bot. If you follow the structure of the skeleton code, you should
not have to make any major changes here to get your bot on line.

However you should at least rename faq_bot_skeleton.py, which means you'll have
to change the import line below.

Note that the bot defined here will respond to EVERY message in every server it
is invited to. It is possible to have it only respond to messages that are
@ it, or only to private messages instead. I will leave it to you to figure that
out!

If you adapt this code, add yourself below as author and rewrite this header
comment from scratch. Make sure you properly comment all classes, methods
and functions as well. See the Resources folder on Canvas for documentation
standards.

YOUR NAME AND DATE
Sam Scott, Mohawk College, May 2023
"""
import discord
from faq_bot_skeleton import *

## MYClient Class Definition

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        # get the utterance and generate the response
        utterance = message.content
        intent = understand(utterance)
        response = generate(intent)

        # send the response
        await message.channel.send(response)

## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()
client.run(token)