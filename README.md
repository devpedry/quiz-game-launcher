# Quiz Game Launcher

A simple Python launcher that requires the user to answer a trivia question before opening a game.

The project fetches a random multiple-choice question from the Open Trivia DB API. If the answer is correct, the selected game launches normally. If the answer is incorrect, a shutdown command is triggered after a short delay.

## Features

* Fetches random quiz questions from a public API
* Displays shuffled multiple-choice answers
* Launches a game executable on correct answer
* Triggers a system shutdown on incorrect answer
* Basic error handling for invalid input and connection issues

## Technologies

* Python
* Requests
* Open Trivia DB API

## Usage

1. Set the game executable path in `GAME_PATH`
2. Run the script:

   ```bash
   python main.py
   ```
3. Answer the quiz correctly to launch the game

> **Warning:** An incorrect answer triggers a shutdown command after 10 seconds.
