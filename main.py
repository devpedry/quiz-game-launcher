import os
import subprocess
import html
import requests
import random
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog



# --- CONFIGURATIONS ---
GAME_PATH = r'E:\SteamLibrary\steamapps\common\War Thunder\launcher.exe' 
API_URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
DIFFICULTY_SETTINGS = {'easy': 1, 'medium': 2, 'hard': 3}
SHUTDOWN_DELAY = 10
ENABLE_SHUTDOWN = True



# --- FUNCTIONS ---

def browse_file():
    """ Opens a dialog to select the game executable """
    filename = filedialog.askopenfilename(title="Select Game Launcher", filetypes=[("Executable files", "*.exe")])
    if filename:
        path_var.set(filename)

def get_quiz(difficulty): 
    """ Fetches a quiz question from the Open Trivia Database API """
    url = f'{API_URL}&difficulty={difficulty}'
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    
    if not data.get('results'):
        raise ValueError("No questions returned from API")


    question = html.unescape(data['results'][0]['question'])
    correct_answer = html.unescape(data['results'][0]['correct_answer'])
    incorrect_answers = [html.unescape(ans) for ans in data['results'][0]['incorrect_answers']]
    
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)
    
    return question, options, correct_answer


def ask_question_gui(question, options, correct_answer, current, total):
    options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
    
    prompt = f"Question {current} of {total}\n\n{question}\n\n{options_text}"

    choice = simpledialog.askinteger(
        "Quiz Challenge",
        prompt,
        minvalue=1,
        maxvalue=len(options)
    )

    # Usuário cancelou
    if choice is None:
        return None

    if options[choice - 1] == correct_answer:
        messagebox.showinfo("Result", "Correct!")
        return True
    else:
        messagebox.showerror(
    "Result",
    f"Wrong!\n\nCorrect answer:\n{correct_answer}"
)
        return False
    

def play_game():
    """ Main game logic using GUI dialogs """
    difficulty = difficulty_var.get()
    current_game_path = path_var.get()

    if not current_game_path:
        messagebox.showerror("Error", "Please select a valid game executable path.")
        return

    if not os.path.isfile(current_game_path):
        messagebox.showerror("Error", "Invalid executable path.")
        return


    question_count = DIFFICULTY_SETTINGS[difficulty]
    score = 0

    for current_question in range(question_count):
        try:
            question, options, correct_answer = get_quiz(difficulty)
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch quiz question. Check your internet.")
            return

        result = ask_question_gui(
            question,
            options,
            correct_answer,
            current_question + 1,
            question_count
        )

        if result is None:
            return

        if result:
            score += 1

    if score == question_count:
        messagebox.showinfo("Victory", "All answers correct! Launching the game...")
        try:
            subprocess.Popen([current_game_path])
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch at {current_game_path}:\n{e}")
    else:
        messagebox.showwarning("System Failure", f"Score: {score}/{question_count}. Shutdown initiated!")

        if ENABLE_SHUTDOWN:
            subprocess.Popen(['shutdown', '/s', '/t', str(SHUTDOWN_DELAY)]) #yes, this will actually shutdown the computer after the delay. Use with caution
        else:
            messagebox.showinfo("Dev Mode", "Shutdown is disabled in this version. No harm will come!")





    

# --- GUI SETUP ---
root = tk.Tk()
root.title("Game Quiz Launcher")
root.geometry("450x300") 

path_var = tk.StringVar(value=GAME_PATH)
difficulty_var = tk.StringVar(value="medium")

# Layout
tk.Label(root, text="GAME EXECUTABLE PATH:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Entry(root, textvariable=path_var, width=50).pack(pady=2)
tk.Button(root, text="BROWSE", command=browse_file).pack(pady=5)

tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=10) # Separator

tk.Label(root, text="SELECT DIFFICULTY:").pack()
# Difficulty selection buttons
frame_diff = tk.Frame(root)
frame_diff.pack()
tk.Button(frame_diff, text="Easy", width=10, command=lambda: difficulty_var.set("easy")).pack(side="left", padx=2)
tk.Button(frame_diff, text="Medium", width=10, command=lambda: difficulty_var.set("medium")).pack(side="left", padx=2)
tk.Button(frame_diff, text="Hard", width=10, command=lambda: difficulty_var.set("hard")).pack(side="left", padx=2)

tk.Label(root, textvariable=difficulty_var, fg="blue", font=("Arial", 10, "italic")).pack(pady=5)

# Start Button
tk.Button(root, text="START QUIZ & PLAY", bg="green", fg="white", font=("Arial", 12, "bold"), 
          height=2, width=20, command=play_game).pack(pady=20)

root.mainloop()