from pathlib import Path

import matplotlib.pyplot as plt

ADC_VALUES = [
    0, 40, 79, 140, 210, 270, 332, 386, 436, 481, 524, 564, 599, 632, 662,
    689, 714, 738, 761, 781, 800, 816, 833, 847, 859, 873, 885, 895, 904, 913,
    922, 930, 936, 942, 949, 955, 959, 964, 968, 972, 976, 979, 983, 985, 988,
    991, 993, 994, 996, 999, 1000, 1002, 1003, 1005, 1006, 1006, 1008, 1009,
    1009, 1011, 1011, 1012, 1012, 1013, 1014, 1015, 1015, 1015, 1015, 1015,
    1016,
]

TARGET_ADC = 1016
T5TAU_SECONDS = 1.5460
TAU_SECONDS = 0.3092


def main() -> None:
    sample_index = list(range(len(ADC_VALUES)))

    plt.figure(figsize=(10, 5))
    plt.plot(sample_index, ADC_VALUES, marker="o", markersize=3, linewidth=1.5, label="ADC medido")
    plt.axhline(TARGET_ADC, color="red", linestyle="--", linewidth=1.2, label=f"Objetivo 5τ ({TARGET_ADC})")

    plt.title("Carga RC hasta 5τ (~99.3%)")
    plt.xlabel("Muestra")
    plt.ylabel("Valor ADC")
    plt.ylim(0, 1023)
    plt.grid(alpha=0.3)
    plt.legend()

    text = f"t5τ = {T5TAU_SECONDS:.4f} s\nτ ≈ {TAU_SECONDS:.4f} s"
    plt.text(0.02, 0.98, text, transform=plt.gca().transAxes, va="top", bbox={"facecolor": "white", "alpha": 0.8})

    output_path = Path(__file__).resolve().parents[1] / "rc_charge_plot.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Gráfica guardada en: {output_path}")


if __name__ == "__main__":
    main()
