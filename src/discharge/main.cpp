#include <Arduino.h>

const int chargePin = 13;
const int analogPin = A0;

unsigned long startTime;
unsigned long endTime;
float timeSeconds;

const int highThreshold = 1016;
const int lowThreshold = 7;

void setup() {
  pinMode(chargePin, OUTPUT);
  digitalWrite(chargePin, LOW);
  Serial.begin(9600);

  Serial.println("--- Medidor RC: Descarga (5 Tau) ---");
  Serial.println("Conectando para ciclo automatico de carga y descarga.");
  delay(1500);
}

void loop() {
  Serial.println("Cargando capacitor al maximo...");
  digitalWrite(chargePin, HIGH);

  int sensorValue = 0;
  while (sensorValue < highThreshold) {
    sensorValue = analogRead(analogPin);
    delay(2);
  }

  delay(100);

  Serial.println("Iniciando descarga...");
  startTime = micros();
  digitalWrite(chargePin, LOW);

  Serial.println("adc:\ttarget_low:");
  sensorValue = analogRead(analogPin);
  while (sensorValue > lowThreshold) {
    sensorValue = analogRead(analogPin);
    Serial.print("adc:");
    Serial.print(sensorValue);
    Serial.print("\ttarget_low:");
    Serial.println(lowThreshold);
    delay(10);
  }

  endTime = micros();
  timeSeconds = (endTime - startTime) / 1000000.0;

  Serial.print("Tiempo para descargar a 5 Tau (~0.7%): ");
  Serial.print(timeSeconds, 4);
  Serial.println(" segundos.");

  Serial.print("Tau estimado descarga (t5tau/5): ");
  Serial.print(timeSeconds / 5.0, 4);
  Serial.println(" segundos.");

  Serial.print("t5tau_desc_s:");
  Serial.print(timeSeconds, 4);
  Serial.print("\ttau_desc_est_s:");
  Serial.println(timeSeconds / 5.0, 4);

  Serial.println("------------------------------------");
  delay(3000);
}
