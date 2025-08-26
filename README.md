# Temperature-monitoring-system-using-Arduino-UNO
A Temperature Monitoring System using Arduino UNO is a simple embedded project that measures ambient temperature with a sensor and displays or logs the data. Here’s a short overview:  🔧 Components Needed  Arduino UNO  Temperature Sensor (LM35, DHT11/DHT22, or DS18B20)  16x2 LCD (or OLED) display / Serial Monitor  Resistors, jumper 
## ⚙️ Working Principle

The sensor (e.g., LM35) generates an analog voltage proportional to temperature.

LM35: 10 mV per °C

DHT11/DHT22: Digital signal with temperature & humidity

Arduino UNO reads the sensor data using its ADC (analog-to-digital converter) or digital pin.

The measured temperature is converted into readable °C/°F values.

Output is displayed on an LCD, OLED, or the Serial Monitor.

(Optional) System can trigger alerts if temperature crosses thresholds.
