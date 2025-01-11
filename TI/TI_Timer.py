from machine import Pin, Timer, I2C, UART
import time
import lcd_api
from pico_i2c_lcd import I2cLcd
import neopixel
import math
import utime
import machine

# Stel seriële communicatie in
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))  # Pas aan voor jouw Pico-pinnen

# Pins setup for buttons
button_pin = Pin(17, Pin.IN, Pin.PULL_UP)
btn_hour = Pin(21, Pin.IN, Pin.PULL_UP)
btn_min = Pin(20, Pin.IN, Pin.PULL_UP)
btn_sec = Pin(19, Pin.IN, Pin.PULL_UP)
btn_reset = Pin(16, Pin.IN, Pin.PULL_UP)
btn_power = Pin(12, Pin.IN, Pin.PULL_UP)

# Pin setup for LCD
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Pin setup for Neopixel
num_pixels = 8
np_pin = Pin(13, Pin.OUT)
pixels = neopixel.NeoPixel(np_pin, num_pixels)

# Pin setup for distance sensor
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

# Timer variables
timer_seconds = 0
total_time = 0
is_running = False
last_press_time = 0

# Set lcd text to default 00:00:00
lcd.clear()
lcd.putstr("Timer: 00:00:00")

# Timer object
timer = Timer()

# Process incoming serial data
def process_serial_data():
    global timer_seconds
    try:
        data = input()
        int(data)
        if int(data) <= 3600:
            received_seconds = 3600
        elif data > 21600:
            received_seconds = 21600
        else:
            received_seconds = data
        timer_seconds = received_seconds
        update_display()
    except ValueError:
        print(e)

# Measure distance 
def measure_distance():
    global is_running
    trigger.low()
    time.sleep(1)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    
    # Calculate the distance in cm
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    
    # Pauzeer de timer als de afstand groter dan 50 cm
    if distance > 50 and is_running:
        is_running = False
        timer.deinit()  # Deinitialize timer
        uart.write("Timer gepauzeerd door afstandssensor\n")  # Bericht naar de pc sturen
        print("Timer gepauzeerd door afstandssensor")
    
    return distance

# Update NeoPixels based on remaining time
def update_neopixels(total_time, remaining_time):
    num_lights_on = math.ceil((remaining_time / total_time) * num_pixels)

    # Turn off all pixels
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)

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

# Format time in HH:MM:SS format
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

# Adjust time on timer
def add_time(seconds):
    global timer_seconds
    timer_seconds += seconds
    update_display()

# Start or pause the timer
def toggle_timer(pin):
    global is_running, last_press_time, timer, timer_seconds, total_time
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_press_time) > 200:
        last_press_time = current_time
        if is_running:
            # Pauzeer timer
            timer.deinit()
            is_running = False
            uart.write("Timer gepauzeerd\n")  # Bericht naar de pc sturen
            print("Timer gepauzeerd")
        else:
            # Start timer
            total_time = timer_seconds
            timer.init(period=1000, mode=Timer.PERIODIC, callback=update_timer)
            is_running = True
            uart.write("Timer gestart\n")  # Bericht naar de pc sturen
            print("Timer gestart")

# Update timer display on the LCD
def update_timer(t):
    global timer_seconds
    if timer_seconds > 0:
        timer_seconds -= 1
        print(f"Tijd over: {timer_seconds} seconden")
        update_display()
        update_neopixels(total_time, timer_seconds)
    else:
        # Set pixels to red when the time is up
        for i in range(num_pixels):
            pixels[i] = (50, 0, 0)
        pixels.write()

        print("Timer is afgelopen!")
        lcd.clear()
        lcd.putstr("Tijd is om!")
        time.sleep(2)
        timer.deinit()
        reset_pico(12)
        time.sleep(1)
        lcd.clear()
        lcd.putstr("Timer: 00:00:00")
        global is_running
        is_running = False

# Update LCD display with current remaining time
def update_display():
    formatted_time = format_time(timer_seconds)
    distance = round(measure_distance(), 2)
    lcd.clear()
    lcd.putstr(f"Timer: {formatted_time}")
    # lcd.move_to(0, 1)
    # lcd.putstr(f"Distance: {distance}")

# Reset timer
def reset_timer(pin):
    global timer_seconds, is_running
    timer_seconds = 0
    is_running = False
    timer.deinit()

    # Show feedback on LCD
    lcd.clear()
    lcd.putstr("Timer resetten")
    time.sleep(1)

    lcd.clear()
    lcd.putstr("Timer: 00:00:00")

# Reset pico 
def reset_pico(pin):
    lcd.clear()
    lcd.putstr("Resetting")        
    time.sleep(3)
    machine.reset()

# Associate button interrupts with functions
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=toggle_timer)
btn_reset.irq(trigger=Pin.IRQ_FALLING, handler=reset_timer)
btn_power.irq(trigger=Pin.IRQ_FALLING, handler=reset_pico)

# Associate button interrupts with time adjustments
btn_hour.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: add_time(3600))
btn_min.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: add_time(60))
btn_sec.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: add_time(1))

try:
    print("Wachten op seriële data...")
    # Get serial data
    process_serial_data()
    
    while True:    
        measure_distance()
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Programma gestopt")
    timer.deinit()




