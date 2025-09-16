#Matthew Lomelin
import time
import threading
from RPLCD.i2c import CharLCD
import keyboard  #Requires sudo

#LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)

rpm = 800
speed = 0
gear = 1
max_gear = 5
min_gear = 1

gear_ratios = [0, 30, 60, 90, 120, 150]
idle_rpm = 800
max_rpm = 6500
upshift_rpm = 5000
downshift_rpm = 1500
acceleration = 100
deceleration = 150
rpm_speed_ratio = 0.015

lock = threading.Lock()

def update_lcd():
    while True:
        with lock:
            lcd.clear()
            lcd.write_string(f"Gear:{gear} RPM:{int(rpm)}")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Speed:{speed:.1f} mph")
        time.sleep(0.2)

def update_terminal():
    while True:
        with lock:
            print(f"Gear: {gear} | Speed: {speed:.1f} mph | RPM: {int(rpm)}")
        time.sleep(0.2)

def update_state():
    global rpm, speed, gear
    while True:
        time.sleep(0.1)
        with lock:
            if keyboard.is_pressed("up"):
                if rpm < max_rpm:
                    rpm += acceleration * 0.1
                speed = min(speed + (rpm_speed_ratio * acceleration * 0.1), gear_ratios[gear])
            else:
                if rpm > idle_rpm:
                    rpm -= deceleration * 0.1
                else:
                    rpm = idle_rpm
                if speed > 0:
                    speed -= (rpm_speed_ratio * deceleration * 0.1)
                    if speed < 0:
                        speed = 0

            # Automatic upshift
            if rpm >= upshift_rpm and gear < max_gear:
                gear += 1
                rpm -= 2000
                if rpm < idle_rpm:
                    rpm = idle_rpm

            #Automatic downshift
            elif rpm <= downshift_rpm and gear > min_gear and speed < gear_ratios[gear - 1] - 5:
                gear -= 1
                rpm *= (gear_ratios[gear + 1] / gear_ratios[gear])
                if rpm > max_rpm:
                    rpm = max_rpm

            #Manual override
            if keyboard.is_pressed("right") and gear < max_gear:
                gear += 1
                rpm -= 1500
                if rpm < idle_rpm:
                    rpm = idle_rpm
                time.sleep(0.3)

            if keyboard.is_pressed("left") and gear > min_gear:
                gear -= 1
                rpm *= (gear_ratios[gear + 1] / gear_ratios[gear])
                if rpm > max_rpm:
                    rpm = max_rpm
                time.sleep(0.3)

threading.Thread(target=update_terminal, daemon=True).start()
threading.Thread(target=update_lcd, daemon=True).start()
update_state()
