import serial
from threading import Thread
import time


def get_timer_status(update_status_callback):
    # Lees de timerstatus van de Raspberry Pi Pico en gebruik een callback om de GUI te updaten.
    try:
        # Open de seriële poort
        ser = serial.Serial('COM3', 115200, timeout=1)
        print("Wachten op berichten van de Raspberry Pi Pico...")

        while True:
            # Controleer of er gegevens zijn ontvangen
            if ser.in_waiting > 0:
                # Lees het bericht en decodeer
                message = ser.readline().decode('utf-8').strip()
                print(f"Ontvangen bericht: {message}")

                update_status_callback(message)
                time.sleep(1)

    except Exception as e:
        print(f"Fout bij lezen van timerstatus: {e}")
    finally:
        # Sluit de seriële poort bij een fout of programma-einde
        if ser.is_open:
            ser.close()