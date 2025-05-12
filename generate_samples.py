# generate_samples.py

import os
import cv2
from generator import generate_cistercian_image

def main():
    # Garante que a pasta exista
    os.makedirs("samples", exist_ok=True)
    print("Pasta samples/ está em:", os.path.abspath("samples"))

    # Exemplos que queremos gerar
    numbers = [1, 5, 10, 42, 1992, 2023, 9999]
    for n in numbers:
        img, _ = generate_cistercian_image(n)
        path = os.path.join("samples", f"{n}.png")
        success = cv2.imwrite(path, img)
        print(f"{'✔' if success else '✘'} Gerado {path}")

if __name__ == "__main__":
    main()
