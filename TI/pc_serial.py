from serial.tools import list_ports
import serial
from AI.steam_data_main import average_playtime_2weeks

# Get average playtime from average_playtime_2weeks function in steam_data_main.py
data = int(round(average_playtime_2weeks(steam_id='76561198030044972') * 60, 0))
str(data)

def read_serial(port):
    """Read data from serial port and return as string."""
    line = port.read(1000)
    return line.decode()

# Zoek alle seriële poorten
serial_ports = list_ports.comports()

# Print alle gevonden poorten
print("[INFO] Beschikbare seriële poorten:")
for port in serial_ports:
    print(f"Poort: {port.device}, Beschrijving: {port.description}")

# Filter de poorten om automatisch de juiste te vinden (nu met COM in plaats van ttyUSB of cu.usbmodem)
pico_port = None
for port in serial_ports:
    if "COM" in port.device:  # Controleren of het een COM-poort is
        pico_port = port.device
        break

if pico_port:
    print(f"[INFO] Raspberry Pi Pico gevonden op poort {pico_port}")
else:
    print("[ERROR] Geen Raspberry Pi Pico gevonden, controleer je verbinding.")
    exit()

# Open een verbinding met de Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    if serial_port.isOpen():
        print(f"[INFO] Gebruik seriële poort {serial_port.name}")
    else:
        print(f"[INFO] Seriële poort openen {serial_port.name}...")
        serial_port.open()

    try:
        # Verzend de data naar de Pico
        while True:
            data_to_send = f"{data}\r"
            serial_port.write(data_to_send.encode())
            pico_output = read_serial(serial_port)
            pico_output = pico_output.replace('\r\n', ' ')
            print("[PICO] " + pico_output)
            break

    except KeyboardInterrupt:
        print("[INFO] Ctrl+C gedetecteerd. Beëindigen.")
    finally:
        # Sluit de verbinding met de Pico
        serial_port.close()
        print("[INFO] Seriële poort gesloten. Tot ziens.")
