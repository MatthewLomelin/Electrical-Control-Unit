
"""
keyboard_input.py
Minimal wrapper around curses for non-blocking key reads.
"""
import curses
from typing import Optional

KEY_UP = 'UP'
KEY_DOWN = 'DOWN'
KEY_LEFT = 'LEFT'
KEY_RIGHT = 'RIGHT'
KEY_PLUS = '+'
KEY_MINUS = '-'
KEY_QUIT = 'q'
KEY_UNKNOWN = None

class CursesInput:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)      # Non-blocking getch
        self.stdscr.keypad(True)       # Translate arrow keys
        curses.curs_set(0)             # Hide cursor

    def read_key(self) -> Optional[str]:
        try:
            ch = self.stdscr.getch()
        except Exception:
            return KEY_UNKNOWN

        if ch == -1:
            return KEY_UNKNOWN

        if ch in (curses.KEY_UP, 65):    # 65 sometimes from ESC seq
            return KEY_UP
        if ch in (curses.KEY_DOWN, 66):
            return KEY_DOWN
        if ch in (curses.KEY_LEFT, 68):
            return KEY_LEFT
        if ch in (curses.KEY_RIGHT, 67):
            return KEY_RIGHT

        # Printable keys
        if ch in (ord('+'), ord('=')):   # allow '=' as '+' on some keyboards
            return KEY_PLUS
        if ch == ord('-'):
            return KEY_MINUS
        if ch in (ord('q'), ord('Q')):
            return KEY_QUIT

        return KEY_UNKNOWN
