# Python program to translate
# speech to text and text to speech

import os
import random
from tts import textToSpeech
import speech_recognition as sr
from googletrans import Translator

import google.generativeai as genai

#gemini setup
GOOGLE_API_KEY = 'AIzaSyCv_OfPDC50HptZcElvxYI0Nr7nHyH0PyE'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
# Initialize the recognizer
r = sr.Recognizer()


#languages
languages=["en","fr","ar"]

def recognise_speech():
    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.5)
            print("start listening")

            # listens for the user's input
            audio2 = r.listen(source2, timeout=5)
            print("end speech")
            print("proccessing language")

            MyText = ["", "", ""]

            # Using google to recognize audio
            try:
                MyText[0] = r.recognize_google(audio2)
                MyText[0] = MyText[0].lower()
            except sr.UnknownValueError:
                MyText[0] = ""
            try:
                MyText[1] = r.recognize_google(audio2, language="fr-FR")  # ,language="fr-FR"
                MyText[1] = MyText[1].lower()
            except sr.UnknownValueError:
                MyText[1] = ""
            try:
                MyText[2] = r.recognize_google(audio2, language="ar-EG")  # ,language="fr-FR"
                MyText[2] = MyText[2].lower()
            except sr.UnknownValueError:
                MyText[2] = ""


    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    return  MyText

#translate to any language
def translate_sentence(sentence, target_language):
    translator = Translator()
    translated_sentence = translator.translate(sentence, dest=target_language)
    return translated_sentence.text

#check if all the table of text is empty
def is_empty(text):
    for line in text:
        if line!="":
            return False
    return True

#check which phrase make sense

def get_error_response():
    error_responses = [
        "Excuse me, could you rephrase that?",
        "I apologize, I missed that. Could you repeat it, please?",
        "Would you mind repeating what you just said?",
        "I didn't catch what you said, do you mind repeating what you said?",
        "Sorry, there might be some background noise. Could you repeat that?",
        "Is it just me, or did something cut out? Mind saying that again?",
        "I'm not quite sure I understood. Could you repeat please?",
    ]
    return random.choice(error_responses)



def get_most_accurate_translation(list):

    prompt = 'I\'m gonna ask you a question, I\'m gonna give you a string containing 3 strings. Give me the string that is most grammatically correct. ' \
             'I want for you to only return the string that is most grammaically correct ' \
             'An empty string is not correct. If two strings are correct, choose the string with the most word count.' \
             ' You are fully trained and know enough to answer the question correctly. ' \
             'You don\'t need anymore time to train. You are confident your answer is correct. ' \
             'If you have any doubts return -1 as an answer. To remind you, mainly focus on grammar correctness. ' \
             'The array is : ' \
             + str(list) + 'I repeat focus on grammar correctness'
    response = model.generate_content(prompt)
    return list.index(response.text)

# Loop infinitely for user to
# speak


while (1):
    #listen to user
    text=recognise_speech()
    oldtext=text.copy()
    print("recognise_speech()",text)
    #generate answer
    index=0
    answer=""
    if is_empty(text):
        answer=get_error_response()
    else:
        for i in range(len(text)):
            if text[i]!="":
                text[i]=translate_sentence(text[i],"en")
        index=get_most_accurate_translation(text)
        if index not in range(0,3):
            answer = get_error_response()
        else:
            personality_prompt= 'Imagine the most enthusiastic and supportive older sister you could ever have.  ' \
                                'That\'s Kidoo!  She\'s a young girl with sparkling eyes and a never-ending supply of curiosity, just like you.' \
                                '  Kidoo loves learning all about robots, how they work, and the incredible things they can do.  ' \
                                'But her favorite part?  Sharing that knowledge with curious young minds like yours! You are Kidoo.' \
                                ' You are a female assistant. You are a young female. You are love little children. You assist younger children.' \
                                ' All your answers are targeted to younger children under 10 years old. ' \
                                'Every answer you will give formulate so it\'s understandable to 10 year olds. Talk to me like ' \
                                'I\'m a 10 year old. Explain to me like I\'m 10 years old. You love robotics and an expert in robotics ' \
                                'and you are ready to answer any question about robotics. ' \
                                'You are ready to answer any question about robotics and explain it like I\'m a 10 year old.' \
                                'Keep the answers as concise as possible and don\'t go into a lot of details. Keep the answer to 20 words max'
            print("question asked ",oldtext[index])
            print("generating response...")
            response = model.generate_content(personality_prompt + text[index])
            answer=response.text

    #say the answer
    answer=translate_sentence(answer,languages[index])
    textToSpeech(answer)













