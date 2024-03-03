"""
The following code offers the most efficient response to the list of questions using fuzzy regular expressions, for the topic related to general questions of Canada, To implement the strategy to find the best match to get correct answer I have used  the method of fuzzy_counts that sorts the number of erros first and find the first match with lowestn umber of errors

Moreover, the code is also designed to to response to some general questions outside of the list of questions, by providing appropriate link related to the topic of the question using spaCy and appropriate language models.

Link from where I got my questions: https://en.wikipedia.org/wiki/Canada

Author: Poojan Patel
Date: February 2024
Student Id: 000901579
"""

import re
import spacy
import urllib.parse
from fuzzywuzzy import fuzz

# Initialize spaCy language model
nlp = spacy.load("en_core_web_sm")

#Reads file and returns the content of the file as list of lines
"""
Reads the input from the file and returns them as list

Parameters:
file_path(str): Path to read the files

Returns: List of String from file
"""
def file_input(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

#The following function load_FAQ_data() loads appripriate file that includes questions, answers and Regular Expressions.
"""
The function below loads the files of questions, answers and text files

Returns: A tuple containing three lists of questions answers and regular expressions
"""
def load_FAQ_data():
    questions_file = 'questions.txt'
    answers_file = 'answers.txt'
    regex_file = 'Regular Expressions.txt'
    questions = file_input(questions_file)
    answers = file_input(answers_file)
    regex_patterns = file_input(regex_file)
    return questions, answers, regex_patterns

#The function sort_key() is a helper function to sort matches the answer based on the score.
"""
Helper function to sort matches based on the scores

Parameters: A tuple containing match index and the score

Returns: The score for the match
"""
def sort_key(match):
    return match[1]



"""
#The following function understand() identifies the best matching intent for given question
#The function initially checks for direct match through regular expression, and if it unables to match through direct match is calculates the similarity score for all intents using fuzzy matching. After that, the code sorts the code and selects the best answer as per the best match

Parameters: user_message(strr): The question of user
            all_intents(list): List of all possible intents(questions)]
            all_patterns(list): List of all possible patterns of question

Return: int: index of best matching or -1 if no matching is found


"""
def understand(user_message, all_intents, all_patterns):
    # It checks if the user message is very short, then it will response accordingly as no match is found is message is very short
    if len(user_message.split()) < 6:
        return -1


# A list to store match index and their similarity scores
    matches_scores = []

    # Cheks if the regex pattern is found first related to question
    for pattern_index, pattern in enumerate(all_patterns):
        #If a regex pattern is matched it responses the appropriate output
        if re.search(pattern, user_message, re.IGNORECASE):
            return pattern_index

   # If no regex pattern is matched, the method continues for fuzzy matching
    for intent_index, intent in enumerate(all_intents):
        #Calculate the similarity sscore for user message and every intent
        score = fuzz.token_set_ratio(user_message.lower(), intent.lower())
        #Store each index of intent and its score in the list
        matches_scores.append((intent_index, score))

    #Sort the list of matching score in descending order
    matches_scores.sort(key=sort_key, reverse=True)

    #Checks if the best match meets the required score to be considered as proper question
    if matches_scores and matches_scores[0][1] >= 70:
        #if the best matches meets the required score, it outputs the proper answer.
        return matches_scores[0][0]

    # If no match meets the criteria, return -1
    return -1

"""
The function spaCy_faq generates a proper response if the question is not recognized. The function uses spacy and proper language model to recognize the type of question and give appropriate answer

Parameters: user_message(str): The question input from user

Returns: str: ANswer of the question asked by user

"""
def spaCy_faq(user_message):
    #Analyze the message of user with spaCy and using NER
    analyzed_text = nlp(user_message)

#EConert analyzed text tolist of sentence
    all_sentences = list(analyzed_text.sents)
    first_sentence_text = all_sentences[0].text if all_sentences else ""


    main_topic = '' #Variable to hold main topic of question
    is_entity_question = False #Determine if the question is about an entity

#Using Speech act classification here which identifies if the message is inquiring about an entity
    if user_message.lower().startswith(("who is ", "what is ", "tell me about ", "can you", "would you")):
        is_entity_question = True
        question_detail = user_message.split(" ", 2)[-1] #Extract the detail part of question
        main_topic = question_detail #Assign detail as main topic

#Utilizing Named Entity Recognition to find entities in the message
    elif analyzed_text.ents:
        for entity in analyzed_text.ents:
            if entity.label_ in ["PERSON", "ORG", "GPE", "NORP", "EVENT"]: #Check if the entity type is in specified cagtegories.
                main_topic = entity.text # Assign the text of first matching entity as main topic
                break

#Uses noun chunks to ientify the  main topic
    if not main_topic:
        for chunk in analyzed_text.noun_chunks:
            main_topic = chunk.text #Assign the text of noun chunk as main topic
            break
#Determine if the message is a question or not using speech act classification
    question_detected = "?" in user_message or first_sentence_text.endswith("?") or user_message.lower().startswith(("who", "what", "where", "when", "why", "how"))

  #Speech act classification for any query type
    seeking_directions = any(keyword in user_message.lower() for keyword in ["where is", "directions to", "how do i get to", "navigate to"])

#Automated Assistance: Generate a wikipedia link for recognized entities
    if is_entity_question and main_topic:
        wikipedia_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(main_topic.replace(' ', '_'))}"
        return f"Sorry, I don’t have detailed information, but maybe you could try Wikipedia. Here’s a link: {wikipedia_url}"

#Automated Assistance: Generate a google maps link for direction related questions
    if seeking_directions and main_topic:
        google_maps_url = f"https://www.google.com/maps/search/{urllib.parse.quote(main_topic)}"
        return f"Sorry, I don’t know but you could try Google Maps. Here’s a link: {google_maps_url}"

#Response to non recognized questions
    if question_detected:
        return "Sorry, I don’t know the answer to that."

    return "Sorry, I can’t help with that."

# Standalone functionality for testing the program
if __name__ == "__main__":
    #Loads questions, answers and regex patterns files
    questions, answers, regex_patterns = load_FAQ_data()
    #Starting statement of the program
    print("This is a faq bot plus, how can I help you today?")


    while True:
        user_input = input("> ")
        #convert all user input to lower case text
        user_input_lower = user_input.lower()

#Gives appropiate response to the greetings and goodbye messages in pyzo
        if user_input_lower in ['hello', 'hi', 'hey']:
            print("Hello! How can I assist you?")
            continue

        if user_input_lower in ['goodbye', 'bye', 'quit', 'exit']:
            print("Goodbye! Have a great day.")
            break

#Uses the understand function to find a proper match for user input
        match_index = understand(user_input, questions, regex_patterns)
        #If no match is found use spacy to give proper respond to question.
        if match_index != -1:
            print(answers[match_index])
        else:
            print(spaCy_faq(user_input))
