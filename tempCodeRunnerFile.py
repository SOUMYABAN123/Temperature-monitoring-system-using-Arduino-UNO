import serial
import csv
from datetime import datetime
import os
import logging
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Arduino Sensor Data Logger')
    parser.add_argument('--port', default='COM6', help='Serial port (default: COM7)')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate (default: 9600)')
    parser.add_argument('--file', default='sensor_log.csv', help='CSV output file (default: sensor_log.csv)')
    return parser.parse_args()

def main():
    args = parse_args()
    SERIAL_PORT = args.port
    BAUD_RATE = args.baudrate
    CSV_FILE = args.file

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser, open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            # Write header only if file is empty
            if os.path.getsize(CSV_FILE) == 0:
                writer.writerow(["Timestamp", "Humidity (%)", "Temperature (°C)", "Distance (cm)"])
                logging.info(f"Header written to {CSV_FILE}")

            logging.info(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud. Logging to {CSV_FILE}")

            while True:
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    continue

                parts = line.split(',')
                if len(parts) != 3:
                    logging.warning(f"Malformed line skipped: {line}")
                    continue

                try:
                    humidity, temperature, distance = map(float, parts)

                    # Validate sensor ranges (adjust as per your sensor specs)
                    if not (0 <= humidity <= 100):
                        logging.warning(f"Humidity out of range: {humidity}")
                        continue
                    if not (-40 <= temperature <= 125):
                        logging.warning(f"Temperature out of range: {temperature}")
                        continue
                    if not (0 <= distance <= 400):
                        logging.warning(f"Distance out of range: {distance}")
                        continue

                    timestamp = datetime.now().isoformat()
                    writer.writerow([timestamp, humidity, temperature, distance])
                    file.flush()
                    logging.info(f"Logged: H={humidity}%, T={temperature}°C, D={distance}cm")

                except ValueError:
                    logging.warning(f"Skipping line with conversion error: {line}")

    except serial.SerialException as e:
        logging.error(f"Serial port error: {e}")
    except KeyboardInterrupt:
        logging.info("User interrupted - exiting.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
