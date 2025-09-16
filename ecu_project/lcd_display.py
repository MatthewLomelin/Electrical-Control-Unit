
"""
lcd_display.py
Abstraction over LCD vs. console output.
- If RPLCD is available and USE_LCD=1, prints to a 16x2 LCD.
- Otherwise, prints a one-line console view refreshed in place.
"""
import os
import shutil
import sys
import time

USE_LCD = os.environ.get("USE_LCD", "0") == "1"

class LCDConfig:
    # Adjust these if wiring differs; only used when using RPLCD GPIO backend.
    cols = 16
    rows = 2
    numbering_mode = 'BOARD'  # or 'BCM' (RPLCD constant will be mapped)
    pin_rs = 37
    pin_e = 35
    pins_data = [33, 31, 29, 23]  # D4..D7

class LCDInterface:
    def __init__(self):
        self._impl = None
        if USE_LCD:
            try:
                from RPLCD.gpio import CharLCD
                import RPi.GPIO as GPIO
                mode = GPIO.BOARD if LCDConfig.numbering_mode.upper() == 'BOARD' else GPIO.BCM
                self._impl = CharLCD(
                    numbering_mode=mode,
                    cols=LCDConfig.cols,
                    rows=LCDConfig.rows,
                    pin_rs=LCDConfig.pin_rs,
                    pin_e=LCDConfig.pin_e,
                    pins_data=LCDConfig.pins_data
                )
                self._lcd = True
            except Exception as e:
                # Fall back to console if LCD setup fails
                self._impl = None
                self._lcd = False
        else:
            self._lcd = False

        # Console rendering settings
        self._last_console_len = 0

    def clear(self):
        if self._lcd and self._impl:
            self._impl.clear()
        else:
            # Clear console line (non-destructive to scrollback)
            sys.stdout.write('\r' + ' ' * max(self._last_console_len, 0) + '\r')
            sys.stdout.flush()
            self._last_console_len = 0

    def close(self):
        if self._lcd and self._impl:
            try:
                self._impl.close(clear=True)
            except Exception:
                pass

    def render(self, rpm: int, speed: int, gear: int):
        """Render a 2-line LCD or one-line console status."""
        line1 = f"RPM:{rpm:4d} SPD:{speed:3d}"
        line2 = f"GEAR:{gear}"
        if self._lcd and self._impl:
            self._impl.cursor_pos = (0, 0)
            self._impl.write_string(line1.ljust(LCDConfig.cols)[:LCDConfig.cols])
            self._impl.cursor_pos = (1, 0)
            self._impl.write_string(line2.ljust(LCDConfig.cols)[:LCDConfig.cols])
        else:
            cols = shutil.get_terminal_size((80, 20)).columns
            text = f"{line1}  {line2}   (↑/↓ RPM, ←/→ Gear, +/- Speed, q Quit)"
            # Truncate if too long
            if len(text) > cols:
                text = text[:max(0, cols - 1)]
            sys.stdout.write('\r' + text)
            sys.stdout.flush()
            self._last_console_len = len(text)
