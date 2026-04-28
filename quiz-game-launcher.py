import subprocess
import html
import requests
import random




GAME_PATH = r'E:\SteamLibrary\steamapps\common\War Thunder\launcher.exe' # Change this to your game launcher path



def get_quiz(): # Fetches a quiz question from the Open Trivia Database API
    url = 'https://opentdb.com/api.php?amount=1&type=multiple'

    response = requests.get(url, timeout=5)
    response.raise_for_status()  # will check if the request was successful..
    data = response.json()
    
    question = html.unescape(data['results'][0]['question'])
    correct_answer = html.unescape(data['results'][0]['correct_answer'])
    incorrect_answers = [html.unescape(ans) for ans in data['results'][0]['incorrect_answers']]
    
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)
    
    return question, options, correct_answer




def play_game(): # Main function to play the quiz game. 
    try:
        question, options, correct_answer = get_quiz()
    except requests.RequestException:
        print('Failed to fetch quiz question. Please check your internet connection.')
        return

    
    print(question)

    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    
    try:
        choice = int(input('Type the number of your answer: '))
    except ValueError:
        print('Invalid input.')
        return
    
    if choice < 1 or choice > len(options):
        print("Invalid option.")
        return
    
    if options[choice - 1] == correct_answer:
        print('Correct answer! Launching the game...')
        try:
            subprocess.Popen([GAME_PATH])
        except FileNotFoundError:
            print(f"Failed to launch the game: Game executable not found at {GAME_PATH}. Please check the path and try again.")
    else:
        print('Wrong answer. System shutdown in 10 seconds...')
        subprocess.Popen(['shutdown', '/s', '/t', '10']) #yes, this will shut down your computer if you get the answer wrong, so be careful.


if __name__ == "__main__":
    play_game()


