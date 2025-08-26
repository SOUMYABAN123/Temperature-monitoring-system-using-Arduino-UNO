#include <DHT.h>

// DHT Sensor
#define DHTPIN 2
#define DHTTYPE DHT22

// LED Pins
#define LED_TEMP1 3  // Temperature LED 1 (always on)
#define LED_TEMP2 4  // Temperature LED 2 (on if hot)
#define LED_HUMID 5  // Humidity LED

// Ultrasonic Sensor
#define TRIG_PIN 6
#define ECHO_PIN 7

// Thresholds
#define TEMP_THRESHOLD 25
#define HUMIDITY_THRESHOLD 55

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(LED_TEMP1, OUTPUT);
  pinMode(LED_TEMP2, OUTPUT);
  pinMode(LED_HUMID, OUTPUT);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Optional: print CSV header once
  Serial.println("Humidity,Temperature,Distance");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT22 read error");
    delay(2000);
    return;
  }

  // Ultrasonic Distance measurement
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  // Print CSV data line
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(distance);

  // Temperature LED logic
  digitalWrite(LED_TEMP1, HIGH); // Always on
  digitalWrite(LED_TEMP2, temperature >= TEMP_THRESHOLD ? HIGH : LOW);

  // Humidity LED logic
  digitalWrite(LED_HUMID, humidity >= HUMIDITY_THRESHOLD ? HIGH : LOW);

  delay(2000); // Wait 2 seconds before next reading
}
