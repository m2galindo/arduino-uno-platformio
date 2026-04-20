# RC Charge/Discharge Time Measurement

Proyecto Arduino que mide el tiempo de carga y descarga de un capacitor en un circuito RC usando un Arduino Uno.

## Características

- **Medición de Carga (5τ):** Mide el tiempo para que el capacitor cargue hasta el ~99.3% (5 constantes de tiempo)
- **Medición de Descarga (5τ):** Mide el tiempo para que el capacitor se descargue hasta el ~0.7%
- **Datos en vivo:** Emite valores ADC durante la carga/descarga para graficar en Serial Plotter
- **Cálculo de τ:** Estima la constante de tiempo RC dividiendo t5τ entre 5

## Estructura del Proyecto

```
.
├── src/
│   ├── charge/
│   │   └── main.cpp          # Sketch de medición de carga
│   └── discharge/
│       └── main.cpp          # Sketch de medición de descarga
├── tools/
│   └── plot_rc.py            # Script Python para graficar datos
├── platformio.ini            # Configuración PlatformIO (dos entornos)
├── requirements.txt          # Dependencias Python
└── README.md                 # Este archivo
```

## Hardware Requerido

- Arduino Uno
- Resistor: ~10 kΩ (ajusta según tu capacitor para τ deseado)
- Capacitor: 10 µF ~ 100 µF (ajusta según τ esperado)
- Cable USB para programar

## Conexiones

```
Pin 13 (Arduino) ----[R]----+---- Capacitor ----+---- GND
                            |
                           [A0] (entrada ADC)
                            |
                           GND
```

## Compilación y Carga

### Ambiente: Carga

```bash
cd /Users/marcoalejandrogalindo/arduino-uno-platformio
pio run -e charge -t upload
```

### Ambiente: Descarga

```bash
cd /Users/marcoalejandrogalindo/arduino-uno-platformio
pio run -e discharge -t upload
```

## Monitoreo en Vivo

Abre el Serial Monitor a 9600 baud para ver los datos:

```bash
pio device monitor -b 9600
```

O usa **Serial Plotter** de Arduino IDE para ver la curva exponencial en tiempo real.

## Ploteo de Datos

Si tienes datos guardados, corre el script Python:

```bash
cd /Users/marcoalejandrogalindo/arduino-uno-platformio
.venv/bin/python tools/plot_rc.py
```

Genera `rc_charge_plot.png` con la gráfica.

## Resultados Esperados

- **Carga (5τ):** t5τ ≈ 1.5 s → τ ≈ 0.31 s
- **Descarga (5τ):** Tiempo similar al de carga (curva invertida)

La constante de tiempo teórica es: **τ = R × C**

## Notas

- Descarga manualmente el capacitor entre ciclos (conecta pin 13 o A0 a GND brevemente)
- Usa `delay(10)` durante medición para estabilizar lecturas ADC
- Para mayor precisión, ajusta el umbral ADC (`threshold = 1016` para 5τ)

## Autor

Proyecto educativo para entender circuitos RC y medición de tiempos en microcontroladores.
