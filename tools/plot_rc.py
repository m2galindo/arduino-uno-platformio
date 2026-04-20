from pathlib import Path
import argparse
import csv

import matplotlib.pyplot as plt

ADC_VALUES = [
    0, 40, 79, 140, 210, 270, 332, 386, 436, 481, 524, 564, 599, 632, 662,
    689, 714, 738, 761, 781, 800, 816, 833, 847, 859, 873, 885, 895, 904, 913,
    922, 930, 936, 942, 949, 955, 959, 964, 968, 972, 976, 979, 983, 985, 988,
    991, 993, 994, 996, 999, 1000, 1002, 1003, 1005, 1006, 1006, 1008, 1009,
    1009, 1011, 1011, 1012, 1012, 1013, 1014, 1015, 1015, 1015, 1015, 1015,
    1016,
]

DISCHARGE_VALUES = [
    1016, 976, 937, 876, 806, 746, 684, 630, 580, 535, 492, 452, 417, 384, 354,
    327, 302, 278, 255, 235, 216, 200, 183, 169, 157, 143, 131, 121, 112, 103,
    94, 86, 80, 74, 67, 61, 57, 52, 48, 44, 40, 37, 33, 31, 28, 25, 23, 22, 20,
    17, 16, 14, 13, 11, 10, 10, 8, 7, 7, 5, 5, 4, 4, 3, 2, 1, 1, 1, 1, 1, 0,
]

TARGET_ADC = 1016
T5TAU_SECONDS = 1.5460
TAU_SECONDS = 0.3092
VREF = 5.0
ADC_MAX = 1023.0


def adc_to_volts(adc_value: int) -> float:
    return adc_value * VREF / ADC_MAX


def build_time_axis(total_seconds: float, sample_count: int) -> list[float]:
    if sample_count < 2:
        return [0.0]
    step = total_seconds / (sample_count - 1)
    return [index * step for index in range(sample_count)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera gráficas RC desde datos CSV.")
    parser.add_argument(
        "--input",
        type=str,
        default="rc_time_volts_data.csv",
        help="Ruta del CSV de entrada (por defecto: rc_time_volts_data.csv).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=".",
        help="Carpeta de salida para PNG/CSV (por defecto: raíz del proyecto).",
    )
    return parser.parse_args()


def try_float(value: str) -> float:
    return float(value.strip())


def try_int(value: str) -> int:
    return int(round(float(value.strip())))


def load_data_from_csv(csv_path: Path) -> tuple[list[float], list[int], list[int]]:
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames or []
        normalized = {header.lower().strip(): header for header in headers}

        rows = list(reader)
        if not rows:
            raise ValueError(f"El CSV está vacío: {csv_path}")

        has_time = "time_s" in normalized
        has_charge_adc = "charge_adc" in normalized
        has_discharge_adc = "discharge_adc" in normalized
        has_adc = "adc" in normalized

        if has_charge_adc:
            charge_key = normalized["charge_adc"]
        elif has_adc:
            charge_key = normalized["adc"]
        else:
            raise ValueError(
                "CSV no válido: requiere columna 'charge_adc' o 'adc'."
            )

        time_axis: list[float] = []
        charge_adc: list[int] = []
        discharge_adc: list[int] = []

        max_reference = TARGET_ADC
        if "target" in normalized:
            target_key = normalized["target"]
            for row in rows:
                value = row.get(target_key, "").strip()
                if value:
                    max_reference = max(max_reference, try_int(value))

        for index, row in enumerate(rows):
            if has_time:
                time_axis.append(try_float(row[normalized["time_s"]]))
            charge_value = try_int(row[charge_key])
            charge_adc.append(charge_value)

            if has_discharge_adc:
                discharge_value = try_int(row[normalized["discharge_adc"]])
            else:
                discharge_value = max_reference - charge_value
            discharge_adc.append(discharge_value)

            if not has_time:
                time_axis = build_time_axis(T5TAU_SECONDS, len(rows))

        return time_axis, charge_adc, discharge_adc


def clamp_adc(values: list[int]) -> list[int]:
    return [max(0, min(int(ADC_MAX), value)) for value in values]


def save_plot(
    time_axis: list[float],
    values: list[float],
    title: str,
    y_label: str,
    legend_label: str,
    output_path: Path,
    reference_value: float | None = None,
    reference_label: str | None = None,
) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(time_axis, values, marker="o", markersize=3, linewidth=1.5, label=legend_label)
    if reference_value is not None and reference_label is not None:
        plt.axhline(reference_value, color="red", linestyle="--", linewidth=1.2, label=reference_label)
    plt.title(title)
    plt.xlabel("Tiempo (s)")
    plt.ylabel(y_label)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_combined_plot(
    time_axis: list[float],
    charge_volts: list[float],
    discharge_volts: list[float],
    output_path: Path,
) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(time_axis, charge_volts, marker="o", markersize=3, linewidth=1.5, label="Carga (V)")
    plt.plot(time_axis, discharge_volts, marker="o", markersize=3, linewidth=1.3, label="Descarga (V)")
    plt.title("Curvas RC: carga y descarga")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.ylim(0, VREF)
    plt.grid(alpha=0.3)
    plt.legend()

    text = f"t5τ = {T5TAU_SECONDS:.4f} s\\nτ ≈ {TAU_SECONDS:.4f} s"
    plt.text(0.02, 0.98, text, transform=plt.gca().transAxes, va="top", bbox={"facecolor": "white", "alpha": 0.8})

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_csv(
    time_axis: list[float],
    charge_adc: list[int],
    discharge_adc: list[int],
    charge_volts: list[float],
    discharge_volts: list[float],
    output_path: Path,
) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "time_s",
            "charge_adc",
            "charge_v",
            "discharge_adc",
            "discharge_v",
        ])
        for row in zip(time_axis, charge_adc, charge_volts, discharge_adc, discharge_volts):
            writer.writerow([
                f"{row[0]:.6f}",
                row[1],
                f"{row[2]:.6f}",
                row[3],
                f"{row[4]:.6f}",
            ])


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (project_root / input_path).resolve()

    output_dir = Path(args.out_dir)
    if not output_dir.is_absolute():
        output_dir = (project_root / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.exists():
        time_axis, charge_adc, discharge_adc = load_data_from_csv(input_path)
    else:
        if len(ADC_VALUES) != len(DISCHARGE_VALUES):
            raise ValueError("ADC_VALUES y DISCHARGE_VALUES deben tener el mismo tamaño.")
        charge_adc = ADC_VALUES
        discharge_adc = DISCHARGE_VALUES
        time_axis = build_time_axis(T5TAU_SECONDS, len(charge_adc))

    charge_adc = clamp_adc(charge_adc)
    discharge_adc = clamp_adc(discharge_adc)

    charge_volts = [adc_to_volts(value) for value in charge_adc]
    discharge_volts = [adc_to_volts(value) for value in discharge_adc]
    target_volts = adc_to_volts(TARGET_ADC)

    charge_plot = output_dir / "rc_charge_plot.png"
    discharge_plot = output_dir / "rc_discharge_plot.png"
    combined_plot = output_dir / "rc_charge_discharge_plot.png"
    csv_output = output_dir / "rc_time_volts_data.csv"

    save_plot(
        time_axis=time_axis,
        values=charge_volts,
        title="Carga RC (Tiempo vs Voltaje)",
        y_label="Voltaje (V)",
        legend_label="Carga (V)",
        output_path=charge_plot,
        reference_value=target_volts,
        reference_label=f"Objetivo 5τ ({target_volts:.3f} V)",
    )
    save_plot(
        time_axis=time_axis,
        values=discharge_volts,
        title="Descarga RC (Tiempo vs Voltaje)",
        y_label="Voltaje (V)",
        legend_label="Descarga (V)",
        output_path=discharge_plot,
    )
    save_combined_plot(
        time_axis=time_axis,
        charge_volts=charge_volts,
        discharge_volts=discharge_volts,
        output_path=combined_plot,
    )
    save_csv(
        time_axis=time_axis,
        charge_adc=charge_adc,
        discharge_adc=discharge_adc,
        charge_volts=charge_volts,
        discharge_volts=discharge_volts,
        output_path=csv_output,
    )

    print(f"CSV de entrada usado: {input_path if input_path.exists() else 'datos embebidos del script'}")
    print(f"Gráfica de carga guardada en: {charge_plot}")
    print(f"Gráfica de descarga guardada en: {discharge_plot}")
    print(f"Gráfica combinada guardada en: {combined_plot}")
    print(f"Datos (tiempo y volts) guardados en: {csv_output}")


if __name__ == "__main__":
    main()
