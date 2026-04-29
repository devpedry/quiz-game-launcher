# Quiz Game Launcher

A Python-based game launcher that requires the user to complete a trivia challenge before opening a game.

The application fetches multiple-choice questions from the Open Trivia DB API. The user selects a difficulty level, answers a set of trivia questions, and the game launches only if all answers are correct. If the user fails the challenge, the system shuts down after a short delay.

---

## Features

* Selectable difficulty levels:

  * **Easy:** 1 question
  * **Medium:** 2 questions
  * **Hard:** 3 questions

* Fetches random trivia questions from the Open Trivia DB API
* Displays shuffled multiple-choice answers
* Tracks score during the challenge
* Launches the game only if all answers are correct
* Shuts down the system after a failed challenge
* Handles invalid input and connection errors
* Centralized configuration for game path, difficulty settings, and shutdown delay

---

## Technologies Used

* Python
* Requests
* Open Trivia DB API

---

## Configuration

Before running the application, configure the following variables in `main.py`:

```python
GAME_PATH = r'path_to_your_game_launcher'

SHUTDOWN_DELAY = 10

DIFFICULTY_SETTINGS = {
    'easy': 1,
    'medium': 2,
    'hard': 3
}
```

* `GAME_PATH`: path to the game executable
* `SHUTDOWN_DELAY`: delay before shutdown in seconds
* `DIFFICULTY_SETTINGS`: number of questions per difficulty

---

## Usage

1. Set the game executable path in `GAME_PATH`
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the launcher:

```bash
python main.py
```

4. Choose a difficulty level
5. Answer all questions correctly to launch the game

---

## Rules

* **Easy:** answer 1 question correctly
* **Medium:** answer 2 questions correctly
* **Hard:** answer 3 questions correctly
* If all answers are correct, the selected game launches
* If any answer is incorrect, the system shuts down after the configured delay

---

## Warning

> If the challenge is failed, the system will shut down after the configured delay.
>
> Default:
>
> ```python
> SHUTDOWN_DELAY = 10
> ```

Use with caution while testing.

---

## Preview

![Quiz Preview](./assets/QuizPreview.png)





## Future Improvements

* GUI with Tkinter
* persistent statistics
* multiple game support