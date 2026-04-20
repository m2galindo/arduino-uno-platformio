#include <Arduino.h>

// Definición de pines
const int chargePin = 13;    // Pin que carga el capacitor
const int analogPin = A0;    // Pin que mide el voltaje

// Variables de tiempo
unsigned long startTime;
unsigned long endTime;
float timeSeconds;

// Umbral para 5 Tau: 1 - e^-5 = 99.33%
// 0.9933 * 1023 ≈ 1016
const int threshold = 1016;

void setup() {
  pinMode(chargePin, OUTPUT);
  digitalWrite(chargePin, LOW); // Aseguramos que empiece descargado
  Serial.begin(9600);

  Serial.println("--- Medidor de Tiempo RC ---");
  Serial.println("Asegurate de que el capacitor este descargado.");
  delay(2000);
}

void loop() {
  Serial.println("Iniciando carga...");

  // 1. Iniciar carga y tomar tiempo
  startTime = micros(); // Usamos micros para mayor precision
  digitalWrite(chargePin, HIGH);

  // 2. Esperar hasta que el voltaje llegue al umbral (5 Tau)
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

  // 3. Calcular tiempo transcurrido
  endTime = micros();
  digitalWrite(chargePin, LOW); // Detener carga

  timeSeconds = (endTime - startTime) / 1000000.0;

  // 4. Mostrar resultados
  Serial.print("Tiempo para llegar a 5 Tau (~99.3%): ");
  Serial.print(timeSeconds, 4);
  Serial.println(" segundos.");

  Serial.print("Tau estimado (t5tau/5): ");
  Serial.print(timeSeconds / 5.0, 4);
  Serial.println(" segundos.");

  // Linea de resumen para Serial Plotter
  Serial.print("t5tau_s:");
  Serial.print(timeSeconds, 4);
  Serial.print("\ttau_est_s:");
  Serial.println(timeSeconds / 5.0, 4);

  Serial.println("------------------------------------");
  Serial.println("Descarga el capacitor para repetir...");

  // Pausa larga para que descargues el capacitor manualmente (o con un cable a GND)
  delay(10000);
}
