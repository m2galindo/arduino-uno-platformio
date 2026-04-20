#include <Arduino.h>

const int chargePin = 13;
const int analogPin = A0;

unsigned long startTime;
unsigned long endTime;
float timeSeconds;

const int threshold = 1016;

void setup() {
  pinMode(chargePin, OUTPUT);
  digitalWrite(chargePin, LOW);
  Serial.begin(9600);

  Serial.println("--- Medidor RC: Carga (5 Tau) ---");
  Serial.println("Asegurate de que el capacitor este descargado.");
  delay(2000);
}

void loop() {
  Serial.println("Iniciando carga...");

  startTime = micros();
  digitalWrite(chargePin, HIGH);

  Serial.println("adc:\ttarget:");
  int sensorValue = 0;
  while (sensorValue < threshold) {
    sensorValue = analogRead(analogPin);
    Serial.print("adc:");
    Serial.print(sensorValue);
    Serial.print("\ttarget:");
    Serial.println(threshold);
    delay(10);
  }

  endTime = micros();
  digitalWrite(chargePin, LOW);

  timeSeconds = (endTime - startTime) / 1000000.0;

  Serial.print("Tiempo para llegar a 5 Tau (~99.3%): ");
  Serial.print(timeSeconds, 4);
  Serial.println(" segundos.");

  Serial.print("Tau estimado (t5tau/5): ");
  Serial.print(timeSeconds / 5.0, 4);
  Serial.println(" segundos.");

  Serial.print("t5tau_s:");
  Serial.print(timeSeconds, 4);
  Serial.print("\ttau_est_s:");
  Serial.println(timeSeconds / 5.0, 4);

  Serial.println("------------------------------------");
  Serial.println("Descarga el capacitor para repetir...");
  delay(10000);
}
