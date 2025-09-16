# Electrical-Control-Unit
A Raspberry Pi based ECU simulator with LCD display and keyboard controls for RPM, speed, and gear values. Built to explore embedded systems, real-time input handling, and automotive data visualization.

DEMO: https://drive.google.com/file/d/1j3NWIalNy_je37wOkSPL3Oaw1GRPsQHg/view?usp=share_link

# ECU Simulation (CLI + optional Raspberry Pi LCD)

A simple ECU-style dashboard you can run from your terminal using arrow keys,
with an optional Raspberry Pi LCD output.

## Controls (terminal)
- **Up / Down**: Increase / Decrease RPM (0–8000)
- **Left / Right**: Gear Down / Gear Up (1–6)
- **+ / -**: Increase / Decrease Speed (0–200 mph)
- **q**: Quit

> Note: Arrow keys adjust **RPM** and **gear**. Use `+` / `-` to adjust **speed**.

## Files
- `ecu_simulation.py` — main loop tying everything together.
- `lcd_display.py` — LCD abstraction. Uses RPLCD on a Raspberry Pi if available; otherwise prints to console.
- `keyboard_input.py` — small wrapper around `curses` key handling.
- `requirements.txt` — currently empty (standard library only). Optional Pi deps listed as comments inside the file.

## Run
```bash
python3 ecu_simulation.py
```

## Raspberry Pi (optional)
If you have a Raspberry Pi with a compatible HD44780 LCD wired via GPIO, install:
```bash
pip install RPi.GPIO RPLCD
```
Then set the environment var before running (so the program prefers LCD output):
```bash
export USE_LCD=1
python3 ecu_simulation.py
```

