from machine import Pin, Timer, I2C
import time
import lcd_api
from pico_i2c_lcd import I2cLcd
import neopixel
import math

# Pin voor buttons
button_pin = Pin(17, Pin.IN, Pin.PULL_UP)
btn_hour = Pin(21, Pin.IN, Pin.PULL_UP)
btn_min = Pin(20, Pin.IN, Pin.PULL_UP)
btn_sec = Pin(19, Pin.IN, Pin.PULL_UP)
btn_reset = Pin(16, Pin.IN, Pin.PULL_UP)

# Pin voor LCD
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.clear()
lcd.putstr("Timer: 00:00:00")

# Pin voor Neopixel
num_pixels = 8
np_pin = Pin(13, Pin.OUT)
pixels = neopixel.NeoPixel(np_pin, num_pixels)

# Timer variabelen
timer_seconds = 0
total_time = 0
is_running = False
last_press_time = 0

timer = Timer()


# Functie starten en pauzeren van de timer
def toggle_timer(pin):
    global is_running, last_press_time, timer, timer_seconds, total_time
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_press_time) > 200:
        last_press_time = current_time
        if is_running:
            # Pauzeer timer
            timer.deinit()
            is_running = False
            print("Timer gepauzeerd")
        else:
            # Start timer
            total_time = timer_seconds
            timer.init(period=1000, mode=Timer.PERIODIC, callback=update_timer)
            is_running = True
            print("Timer gestart")


# Functie om de timer te resetten
def reset_timer(pin):
    global timer_seconds, is_running
    timer_seconds = 0
    is_running = False
    timer.deinit()

    # feedback weergeven op LCD
    lcd.clear()
    lcd.putstr("Timer gereset")
    time.sleep(1)

    # Zet weergaven op standaard tijd
    lcd.clear()
    lcd.putstr("Timer: 00:00:00")
    print("Timer gereset")


# Interrupt voor de start/stop knop. voert onmiddelijk de functie toggle_timer uit als er op de knop gedrukt wordt.
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=toggle_timer)

# Interrupt voor de reset-knop
btn_reset.irq(trigger=Pin.IRQ_FALLING, handler=reset_timer)


# Functie om de neopixels aan en uit te zetten.
def update_neopixels(total_time, remaining_time):
    # Bereken hoeveel lampjes er aan moeten staan op basis van de resterende tijd
    num_lights_on = math.ceil((remaining_time / total_time) * num_pixels)

    # Zet alle pixels uit
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)

    # Update de pixels afhankelijk van de resterende tijd
    for i in range(num_lights_on):
        if i >= 6:
            red, green, blue = 0, 25, 0
        elif i >= 4:
            red, green, blue = 25, 25, 0
        elif i >= 2:
            red, green, blue = 25, 5, 0
        else:
            red, green, blue = 25, 0, 0

        pixels[i] = (red, green, blue)

    pixels.write()


# Functie die de resterende tijd berekend
def update_timer(t):
    global timer_seconds
    if timer_seconds > 0:
        timer_seconds -= 1
        print(f"Tijd over: {timer_seconds} seconden")
        update_display()
        update_neopixels(total_time, timer_seconds)
    else:
        # Zet neopixels op rood
        for i in range(num_pixels):
            pixels[i] = (50, 0, 0)
        pixels.write()

        print("Timer is afgelopen!")
        lcd.clear()
        lcd.putstr("Tijd is om!")
        time.sleep(1)
        timer.deinit()
        lcd.clear()
        lcd.putstr("Timer: 00:00:00")
        global is_running
        is_running = False


def format_time(seconds):
    # Formateer tijd in uren: minuten: seconden, 00:00:00
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"


def update_display():
    formatted_time = format_time(timer_seconds)
    lcd.clear()
    lcd.putstr(f"Timer: {formatted_time}")


# Start de timer
try:
    print("Druk op de knop om de timer te starten of te pauzeren.")

    # Knoppen om de tijd in te stellen
    while True:
        if not btn_hour.value():
            timer_seconds += 3600
            update_display()
        if not btn_min.value():
            timer_seconds += 60
            update_display()
        if not btn_sec.value():
            timer_seconds += 1
            update_display()

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Programma gestopt")
    timer.deinit()

# Bronnen
# https://docs.micropython.org/en/latest/library/machine.Timer.html
# https://docs.micropython.org/en/latest/wipy/tutorial/timer.html


