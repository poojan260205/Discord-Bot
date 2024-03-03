"""
The following code is the code that connects to discord. The code imports all the necessary functions from faq_bot_skeleton so that the bot on discord functions in the same way as it does in the pyzo shell.

The following code handles the connection to discord and generate answers after calling appropriate functions from faq_bot_template. It also handles appropriate response to greetings and goodbye messages in discord.

Author: Poojan Patel
Date: February, 2024
Student id: 000901579

"""
import discord
from faq_bot_skeleton import load_FAQ_data, understand, spaCy_faq


class MyClient(discord.Client):
    #Initialization method for discord client
    """
    The following function __init__ starts the discord client with proper intents and also loads the proper Data
    """
    def __init__(self):
        intents = discord.Intents.default() #intents to handle messages
        intents.message_content = True #Enable message content to read message
        super().__init__(intents=intents)
        #Load FAQ data from appropriate files
        self.questions, self.answers, self.regex_patterns = load_FAQ_data()

    """
    Prints appropriate statement when the connection is made
        """
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    #Method to handle messages and prevent creating infinite loops
    """
    Handles the questions and gives answer appropriately

    Process user messages for greetings and goodbye and also calls understand function and spaCy_function from faq_bot_template and                         gives appropriate answer as per the question asked.
    """
    async def on_message(self, message):

        if message.author == self.user or message.author.bot:
            return

        user_input = message.content #Extract content of message
        user_input_lower = user_input.lower() #Converts message to lowercase to make case insensitive

        # Handle greetings and goodbye messages in discord
        if user_input_lower in ['hello', 'hi', 'hey']:
            await message.channel.send("Hello! How can I assist you?")
            return

        if user_input_lower in ['goodbye', 'bye', 'quit', 'exit']:
            await message.channel.send("Goodbye! Have a great day.")
            return

        #Process user questions through faq data
        match_index = understand(user_input, self.questions, self.regex_patterns)
        #if matching is found give corresponding answer and if not found use spacy function to generate answers
        if match_index != -1:
            response = self.answers[match_index]
        else:
            response = spaCy_faq(user_input)

        await message.channel.send(response)

if __name__ == "__main__":
    client = MyClient()
    #Read the bot token from bot_token.txt file
    with open("bot_token.txt") as file:
        token = file.read().strip()
    client.run(token)
