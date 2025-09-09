import curses
import time
from load_metrical import load_mtw
from get_metrical_embeddings import get_embeddings
from retrieve_metrical_similar import get_judge_context
from create_judge import create_judge
from judge_poem import judge_poem
import os
import json
import random


N_TRIES = 3
WIN_THRESHOLD = 7


def load_screen(stdscr):
    stdscr.clear()
    loading_text = "Performing initial ingestion of the canon..."
    stdscr.addstr(curses.LINES // 2, (curses.COLS - len(loading_text)) // 2, loading_text)
    curses.curs_set(0)
    stdscr.refresh()

    if not os.path.exists("metrical_embeddings.npy"):
        if not os.path.exists("metrical_poetry.jsonl"):
            load_mtw()
        get_embeddings()


def generate_critic(stdscr):
    stdscr.clear()
    loading_text = "Generating a critic..."
    stdscr.addstr(curses.LINES // 2, (curses.COLS - len(loading_text)) // 2, loading_text)
    curses.curs_set(0)
    stdscr.refresh()
    get_judge_context()
    return create_judge()

def main_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(curses.LINES // 2 - 1, (curses.COLS // 2) - 5, "Poetaster")
        stdscr.addstr(curses.LINES // 2 + 2, (curses.COLS // 2) - 5, "1. Play")
        stdscr.addstr(curses.LINES // 2 + 3, (curses.COLS // 2) - 5, "2. Exit")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord("1"):
            critic_desc = generate_critic(stdscr)
            main_game(stdscr, critic_desc)  # Start the game if "Play" is selected
        elif key == ord("2"):
            break  # Exit the game

def main_game(stdscr, critic_desc):
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    input_buffer = []
    attempts_left = 3
    feedback = ""

    with open("authors.json", "rt") as a_in:
        authors = [i for i in list(set(json.load(a_in))) if "?" not in i]
        random.shuffle(authors)

    author_hint = authors.pop()

    curses.curs_set(0)

    while True:
        stdscr.clear()
        stdscr.addstr(1, 1, f"Remaining attempts: {attempts_left}")
        stdscr.addstr(3, 1, f"Write me somthing in the style of {author_hint}", curses.color_pair(1))
        stdscr.addstr(5, 1, feedback, curses.color_pair(1))
        stdscr.addstr(8, 1, "Inscribe below (Press Enter to submit, Ctrl+L for newline):")
        stdscr.addstr(9, 1, "".join(["-"]*curses.COLS))
        
        # Display input buffer
        for idx, line in enumerate(input_buffer):
            stdscr.addstr(10 + idx, 1, line)

        
        # Check for lose condition
        if attempts_left <= 0:
            lose_screen(stdscr)
            return

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_BACKSPACE or key == 127:
            if input_buffer:
                input_buffer[-1] = input_buffer[-1][:-1]  # Remove last character from last line
                if input_buffer[-1] == "":
                    input_buffer.pop()  # Remove empty line

        elif key == 10:  # Enter key
            if len(input_buffer) > 0 and all(line == "" for line in input_buffer):
                continue  # Ignore empty buffer
            stdscr.addstr(10+len(input_buffer), 1, "Calculating your poetic worth...",curses.color_pair(1))
            stdscr.refresh()
            score, feedback = judge_poem(critic_desc, "\n".join(input_buffer))
            stdscr.addstr(10+len(input_buffer), 1, "                                ")
            stdscr.refresh()
            author_hint += f" or maybe {authors.pop()}" if len(authors) > 0 else ""
            if score >= WIN_THRESHOLD:
                win_screen(stdscr)
                return
            else:
                attempts_left -= 1
                feedback = f"I give this a {score}. {feedback}"
                input_buffer = []

        elif key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            continue

        elif key == 12:  # Ctrl+L
            input_buffer.append("")  # Add a new line

        else:
            if len(input_buffer) == 0:
                input_buffer.append("")  # Start with a new line if empty
            input_buffer[-1] += chr(key)  # Add character to the last lines

def win_screen(stdscr):
    stdscr.clear()
    win_text = "Ah, the muses have blessed you with fame eternal!"
    stdscr.addstr(curses.LINES // 2, (curses.COLS - len(win_text)) // 2, win_text)
    stdscr.refresh()
    time.sleep(3)

def lose_screen(stdscr):
    stdscr.clear()
    lose_text = "Try again next time, mute inglorious Milton."
    stdscr.addstr(curses.LINES // 2, (curses.COLS - len(lose_text)) // 2, lose_text)
    stdscr.refresh()
    time.sleep(3)

def main():
    curses.wrapper(load_screen)  # Start with the loading screen
    curses.wrapper(main_menu)     # Show the main menu after loading

if __name__ == "__main__":
    main()