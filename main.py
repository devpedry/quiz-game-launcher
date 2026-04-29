import subprocess
import html
import requests
import random




GAME_PATH = r'E:\SteamLibrary\steamapps\common\War Thunder\launcher.exe' # Change this to your game launcher path

API_URL = 'https://opentdb.com/api.php?amount=1&type=multiple'

DIFFICULTY_SETTINGS = {
    'easy': 1,
    'medium': 2,
    'hard': 3
}

SHUTDOWN_DELAY = 10




def choose_difficulty():
    difficulties = ['easy', 'medium', 'hard']
    
    while True:
        user_input = input('Choose difficulty (1-easy, 2-medium, 3-hard): ').strip()
        
        if user_input in ['1', '2', '3']:
            return difficulties[int(user_input)-1]
        
        print("Invalid option, try again.")

def get_quiz(difficulty): # Fetches a quiz question from the Open Trivia Database API
    url = f'{API_URL}&difficulty={difficulty}'
    

    response = requests.get(url, timeout=5)
    response.raise_for_status()  # will check if the request was successful..
    data = response.json()
    
    question = html.unescape(data['results'][0]['question'])
    correct_answer = html.unescape(data['results'][0]['correct_answer'])
    incorrect_answers = [html.unescape(ans) for ans in data['results'][0]['incorrect_answers']]
    
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)
    
    return question, options, correct_answer




def play_game():
    difficulty = choose_difficulty()
    print(f"Difficulty selected: {difficulty}")

    question_count = DIFFICULTY_SETTINGS[difficulty]

    score = 0

    for current_question in range(question_count):
        print(f"\nQuestion {current_question + 1} of {question_count}")

        try:
            question, options, correct_answer = get_quiz(difficulty)
        except requests.RequestException:
            print('Failed to fetch quiz question. Please check your internet connection.')
            return

        print(question)

        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        while True:
            try:
                choice = int(input('Type the number of your answer: '))

                if 1 <= choice <= len(options):
                    break

                print("Invalid option.")

            except ValueError:
                print("Invalid input.")

        if options[choice - 1] == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print("Wrong answer!\n")

    print(f"You got {score}/{question_count} correct.")

    if score == question_count:
        print('All answers correct! Launching the game...')
        try:
            subprocess.Popen([GAME_PATH])
        except FileNotFoundError:
            print(f"Failed to launch the game: Game executable not found at {GAME_PATH}. Please check the path and try again.")
    else:
        print('You did not answer all questions correctly. System shutdown in 10 seconds...')
        subprocess.Popen(['shutdown', '/s', '/t', str(SHUTDOWN_DELAY)]) # Yes, this will shutdown the system if the user fails the quiz. Use with caution

if __name__ == "__main__":
    play_game()


