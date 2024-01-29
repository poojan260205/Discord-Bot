""" This is a very simple skeleton for a FAQ bot, based on the handout given in
class. Your job is to create your own FAQ bot that can answer 20 questions
using basic string matching. See the handout for more details.

When you create your bot you can adapt this code or start from scratch and
write your own code.

If you adapt this code, add yourself below as author and rewrite this header
comment from scratch. Make sure you properly comment all classes, methods
and functions as well. See the Resources folder on Canvas for documentation
standards.

Source for questions and answers: https://en.wikipedia.org/wiki/Canada
Poojan Patel, Mohawk College, January 2024
"""
import string
from file_input import  file_input

def load_FAQ_data():
    """This method reads questions and answers from files and returns two lists.
    The lists are parallel, meaning that question n pairs with answer n."""
    questions_file = 'questions.txt'
    answers_file = 'answers.txt'

    questions = file_input(questions_file)
    answers = file_input(answers_file)

    return questions, answers

def understand(utterance):
    """
Using the method, utterance undergoes to identify which purpose it matches. Ignoring whitespace, removing punctuation and case insensitivity are used into practice here. If no intent is found the function returns -1
    """

    try:

        standardized_intents = [intent.lower().translate(str.maketrans('', '', string.punctuation)) for intent in intents]
        return standardized_intents.index(utterance.lower().strip().translate(str.maketrans('','',string.punctuation)))
    except ValueError:
       return -1

def generate(intent):
    """This function returns an appropriate response given a user's
    intent."""

    global responses # declare that we will use a global variable

    if intent == -1:
        return "Sorry, I don't know the answer to that!"

    return responses[intent]

## Load the questions and responses
intents, responses = load_FAQ_data()

## Main Function

def main():
    """Implements a chat session in the shell."""
    print("Hello! I know stuff about chat bots. When you're done talking, just say 'goodbye'.")
    print()
    utterance = ""
    while True:
        utterance = input(">>> ")
        if utterance == "goodbye":
            break;
        intent = understand(utterance)
        response = generate(intent)
        print(response)
        print()

    print("Nice talking to you!")

## Run the chat code
# the if statement checks whether or not this module is being run
# as a standalone module. If it is beign imported, the if condition
# will be false and it will not run the chat method.
if __name__ == "__main__":
    main()