import speech_recognition as speechR
import random
import time

def RecognizeSpeech(recognizer, microphone):

    #this basically checks if the arguments given in the function are of the correct type
    if not isinstance(recognizer, speechR.Recognizer):
        raise TypeError("recognizer must be 'Recognizer' instance")
    if not isinstance(microphone, speechR.Microphone):
        raise TypeError("microphone must be 'Microphone' instance")
    
    #we need to adjust microphone for background noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    #we prepare 3 responses and put them in an 'response object'
    response = {
        "succes" : True,
        "error" : None,
        "transcription" : None
    }

    #now we try recognizing the speech in the recording, if not we will catch it in an exception
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except speechR.RequestError:
        response["succes"] = False
        response["error"] = "API could not be reached"
    except speechR.UnknownValueError:
        response["error"] = "unknown error or unable to recognize speech"
    return response

#now we need to initialize the microphone and also create a list were we will store the words in the game
if __name__ == "__main__":
    WORDS = ["ass", "cheesecake", "retard", "orange", "danger", "watermelon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    #initializing mic and recognizer
    recognizer = speechR.Recognizer()
    microphone = speechR.Microphone()

    #getting a random from the list
    word = random.choice(WORDS)

    #we also need to provide instruciton to the user
    instructions = ("I have a word on my mind:\n {words}\n Can you guess wich one?\n").format(words= ','.join(WORDS), n=NUM_GUESSES)
    #perhaps we should also provide some time for the user to read the instructions and words before starting the game
    print(instructions)
    time.sleep(5)

#now we make a loop that takes microphone inputs from the user three times. and also checks the input with the selected word.
for i in range(NUM_GUESSES):
    for j in range(PROMPT_LIMIT):
        print('Guess {}. Speak!'.format(i+1))
        #to define guess we call the function RecognizeSpeech we made above
        guess = RecognizeSpeech(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["succes"]:
            break
        print("I did not understand that, can you try again?\n")

    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        break
    print("You said: {}".format(guess["transcription"]))

    #now we create a statement to check if the user has guessed the correct word and how many attempts are left if any
    correct_guess = guess["transcription"].lower() == word.lower()
    user_has_attempts = i < NUM_GUESSES - 1

    if correct_guess:
        print("Correct! you guessed the right word!")
        break
    elif user_has_attempts:
        print("Incorrect. try again.\n")
    else:
        print("GAME OVER!\n The correct word is {}".format(word))
        break
