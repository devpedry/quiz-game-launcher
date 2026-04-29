# Quiz Game Launcher

A simple Python launcher that requires the user to answer a trivia question before opening a game.

The project fetches a random multiple-choice question from the Open Trivia DB API. If the answer is correct, the game launches normally. If the answer is incorrect, the system shuts down after a short delay.

## Features

* Fetches random quiz questions from a public API
* Displays shuffled multiple-choice answers
* Launches the game on a correct answer
* Shuts down the system after an incorrect answer
* Basic error handling for invalid input and connection issues

## Technologies

* Python
* Requests
* Open Trivia DB API

## Usage

1. Set the game executable path in `GAME_PATH`
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

4. Answer the quiz correctly to launch the game

> **Warning:** An incorrect answer will trigger a system shutdown after 10 seconds

## Preview

![Quiz Preview](./assets/QuizPreview.png)