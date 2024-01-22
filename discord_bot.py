
import discord
import re
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

        if message.channel.name != 'bot-channel':
            return
        # check message content and respond accordingly
        if message.content == 'ping':
            await message.channel.send('pong')


        global msg
        msg = message

## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()

client.run(token)
