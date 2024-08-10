import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the typing test!") #(0, 0, "Hello world!") the number here represent first one for row and second one for column
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0,f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() # .strip() gets rid of any whitespace characters here it is \n

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) # do not delay waiting for a user to hit a key >> key = stdscr.getkey() but by doing this delay we will get an exception on the line key = stdscr.getkey() so we have to handle it
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) #len(current_text) / (time_elapsed / 60) > this gives us characters per minute an we assume avg length of a word is 5 to get the words per minute

        stdscr.clear()      
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try: # This will help the program not getting crashed because of the nodelay
            key = stdscr.getkey()
        except:
            continue

        if key == '\x1b':  # 'ESC' key
            break

        if key in ("KEY_BACKSPACE","\b", "\x7f"):
            if len(current_text) > 0:   
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
        


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #The int 1 here represets the pair we have made of the foreground color and the background color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #The int 2 here represets the pair we have made of the foreground color and the background color
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) #The int 3 here represets the pair we have made of the foreground color and the background color

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You have completed the test. Press any key to continue...")
        key = stdscr.getkey()
        
        if key == '\x1b':  # 'ESC' key
            break

wrapper(main)