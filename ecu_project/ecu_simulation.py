
"""
ecu_simulation.py
Main loop tying together input, state, and display.
"""
import curses
import time

from lcd_display import LCDInterface
from keyboard_input import (
    CursesInput, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_PLUS, KEY_MINUS, KEY_QUIT, KEY_UNKNOWN
)

RPM_MIN, RPM_MAX = 0, 8000
SPD_MIN, SPD_MAX = 0, 200
GEAR_MIN, GEAR_MAX = 1, 6

class ECUState:
    def __init__(self):
        self.rpm = 900   # idle
        self.speed = 0
        self.gear = 1

    def clamp(self):
        self.rpm = max(RPM_MIN, min(RPM_MAX, self.rpm))
        self.speed = max(SPD_MIN, min(SPD_MAX, self.speed))
        self.gear = max(GEAR_MIN, min(GEAR_MAX, self.gear))

def run(stdscr):
    # Setup
    kb = CursesInput(stdscr)
    lcd = LCDInterface()
    state = ECUState()

    rpm_step_small = 100
    rpm_step_big = 250
    spd_step = 5

    last_render = 0.0
    fps = 30.0
    dt_target = 1.0 / fps

    try:
        while True:
            # Input
            key = kb.read_key()
            if key == KEY_QUIT:
                break
            elif key == KEY_UP:
                state.rpm += rpm_step_big if state.rpm >= 3000 else rpm_step_small
            elif key == KEY_DOWN:
                state.rpm -= rpm_step_big if state.rpm >= 3000 else rpm_step_small
            elif key == KEY_RIGHT:
                state.gear += 1
            elif key == KEY_LEFT:
                state.gear -= 1
            elif key == KEY_PLUS:
                state.speed += spd_step
            elif key == KEY_MINUS:
                state.speed -= spd_step

            # Physics-lite: gentle rpm decay, speed drag
            state.rpm = int(state.rpm * 0.999)
            state.speed = max(SPD_MIN, int(state.speed * 0.999))

            state.clamp()

            # Render (limit to ~fps)
            now = time.time()
            if now - last_render >= dt_target:
                lcd.render(state.rpm, state.speed, state.gear)
                last_render = now

            # Sleep a smidge to avoid busy-wait
            time.sleep(0.005)
    finally:
        lcd.clear()
        lcd.close()

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()
