import os
import subprocess
import html
import requests
import random
import tkinter as tk
import json
from pathlib import Path

from tkinter import filedialog, messagebox, simpledialog



# --- CONFIGURATIONS ---
SETTINGS_PATH = Path("data") / ".quiz_launcher.json"
MAX_SAVED = 10
GAME_PATH = r'E:\SteamLibrary\steamapps\common\War Thunder\launcher.exe' 
API_URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
DIFFICULTY_SETTINGS = {'easy': 1, 'medium': 2, 'hard': 3}
SHUTDOWN_DELAY = 10
ENABLE_SHUTDOWN = True
SETTINGS_CACHE = None




''' Save and Load game paths '''

def load_settings():
    global SETTINGS_CACHE
    
    if SETTINGS_CACHE is not None:
        return SETTINGS_CACHE

    if SETTINGS_PATH.exists():
        try:
            SETTINGS_CACHE = json.loads(SETTINGS_PATH.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            SETTINGS_CACHE = {"saved_games": []}
    else:
        SETTINGS_CACHE = {"saved_games": []}

    return SETTINGS_CACHE


def save_settings(settings):
    global SETTINGS_CACHE
    
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding='utf-8')
    
    SETTINGS_CACHE = settings


def get_saved_games():
    return load_settings().get("saved_games", [])


def add_saved_game(path):
    s = load_settings()
    lst = s.get("saved_games", [])
    if path in lst:
        lst.remove(path)
    lst.insert(0, path)
    s["saved_games"] = lst[:MAX_SAVED]
    save_settings(s)


def remove_saved_game(path):
    s = load_settings()
    s["saved_games"] = [p for p in s.get("saved_games", []) if p != path]
    save_settings(s)



def refresh_saved_listbox(listbox):
    """Refresh listbox display and remove invalid paths (only save if changed)"""
    s = load_settings()
    valid_games = [p for p in s.get("saved_games", []) if os.path.isfile(p)]

    # Only save if list changed (removed invalid paths)
    if valid_games != s.get("saved_games", []):
        s["saved_games"] = valid_games
        save_settings(s)

    listbox.delete(0, tk.END)
    for p in valid_games:
        listbox.insert(tk.END, p)


def on_saved_double_click(event=None):
    sel = saved_listbox.curselection()
    if sel:
        path_var.set(saved_listbox.get(sel[0]))


def save_current_path():
    p = path_var.get()
    if not p:
        messagebox.showerror("Error", "No path to save.")
        return

    add_saved_game(p)
    refresh_saved_listbox(saved_listbox)

    messagebox.showinfo("Saved", "Path added to saved games.")


def remove_selected_saved():
    sel = saved_listbox.curselection()
    if not sel:
        messagebox.showerror("Error", "No selection to remove.")
        return

    p = saved_listbox.get(sel[0])
    remove_saved_game(p)

    refresh_saved_listbox(saved_listbox)


def load_last():
    """Load the most recently used game path"""
    saved = get_saved_games()
    if saved:
        path_var.set(saved[0])
    else:
        messagebox.showinfo("Info", "No saved games available.")









# --- FUNCTIONS ---

def browse_file():
    """ Opens a dialog to select the game executable """
    filename = filedialog.askopenfilename(title="Select Game Launcher", filetypes=[("Executable files", "*.exe")])
    if filename:
        path_var.set(filename)

def get_quiz(difficulty): 
    """ Fetches a quiz question from the Open Trivia Database API """
    url = f'{API_URL}&difficulty={difficulty}'
    
    for _ in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            break
        except requests.RequestException:
            continue
    else:
        raise requests.RequestException("Failed to fetch after 3 attempts")
    
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

    # user cancelled
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

    if not current_game_path.lower().endswith(".exe"):
        messagebox.showerror("Error", "Selected file is not a valid executable.")
        return

    if not messagebox.askyesno("Start", "Start quiz challenge now?"):
        return

    question_count = DIFFICULTY_SETTINGS[difficulty]
    score = 0

    for current_question in range(question_count):
        try:
            question, options, correct_answer = get_quiz(difficulty)
        except (requests.RequestException, ValueError):
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
            # Save this path to saved games (move to top)
            try:
                add_saved_game(current_game_path)

                refresh_saved_listbox(saved_listbox)
            except Exception:
                pass
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
root.geometry("600x380") 

path_var = tk.StringVar(value=GAME_PATH)
difficulty_var = tk.StringVar(value="medium")

# Layout
tk.Label(root, text="GAME EXECUTABLE PATH:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Entry(root, textvariable=path_var, width=50).pack(pady=2)
tk.Button(root, text="BROWSE", command=browse_file).pack(pady=5)

# Saved games list and controls
saved_frame = tk.Frame(root)
saved_frame.pack(pady=5, fill='x', padx=10)
tk.Label(saved_frame, text="Saved Games:").pack(anchor='w')
saved_listbox = tk.Listbox(saved_frame, height=5, width=80)
saved_listbox.pack(side='left', fill='x', expand=True)
saved_listbox.bind('<Double-1>', on_saved_double_click)

btn_frame = tk.Frame(saved_frame)
btn_frame.pack(side='right', padx=5)
tk.Button(btn_frame, text="Save Shortcut", command=save_current_path).pack(fill='x', pady=2)
tk.Button(btn_frame, text="Remove Selected", command=remove_selected_saved).pack(fill='x', pady=2)
tk.Button(btn_frame, text="Load Last", command=load_last).pack(fill='x', pady=2)

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

# populate saved games list before showing UI
try:
    refresh_saved_listbox(saved_listbox)
except Exception:
    pass

root.mainloop()
