import os
import cv2
import numpy as np
import pandas as pd

# 1) IMPORTA A FUNÇÃO DE GERAÇÃO DO SEU generator.py
from generator import generate_cistercian_image


# parâmetros — devem bater com generator.py
CELL_SIZE = 40
MARGIN    = 20


def list_images(folder: str):
    """Retorna lista de arquivos de imagem na pasta"""
    return sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith(('.png','jpg','jpeg','bmp'))
    )


def recognize_image(path: str):
    """
    Reconhece um número Cisterciense já gerado:
    1) carrega, binariza
    2) para cada quadrante (unidades, dezenas, centenas, milhares),
       faz template‐matching com os dígitos 1–9 gerados on‐the‐fly
    3) monta o número, reencontra as ROIs e devolve tudo
    """
    # 1) carrega imagem em tons de cinza
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    #  binariza invertido (traço=branco aqui)
    _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # 2) define coordenadas fixas dos 4 quadrantes
    left_x  = (MARGIN,           MARGIN + 2*CELL_SIZE)
    right_x = (MARGIN + CELL_SIZE, MARGIN + 3*CELL_SIZE)
    top_y   = (MARGIN,           MARGIN + 2*CELL_SIZE)
    bot_y   = (MARGIN + 2*CELL_SIZE, MARGIN + 4*CELL_SIZE)
    coords = {
        0: (*right_x, *top_y),   # unidades (UR)
        1: (*left_x,  *top_y),   # dezenas (UL)
        2: (*right_x, *bot_y),   # centenas (LR)
        3: (*left_x,  *bot_y),   # milhares (LL)
    }

    digits = []
    # para cada posição decimal, detecta o melhor template
    for pos in range(4):
        x1,x2,y1,y2 = coords[pos]
        roi = thresh[y1:y2, x1:x2]
        if cv2.countNonZero(roi) == 0:
            # nenhum traço → dígito zero
            digits.append(0)
            continue

        best_score = -1.0
        best_digit = 0
        # testa 1..9 gerando cada dígito on‐the‐fly
        for d in range(1,10):
            # gera só aquele dígito na posição pos
            num = d * (10**pos)
            template_img, _ = generate_cistercian_image(
                num, cell_size=CELL_SIZE, margin=MARGIN
            )
            temp_roi = template_img[y1:y2, x1:x2]
            _, temp_bin = cv2.threshold(temp_roi, 200, 255, cv2.THRESH_BINARY_INV)
            res = cv2.matchTemplate(roi, temp_bin, cv2.TM_CCOEFF_NORMED)
            _, score, _, _ = cv2.minMaxLoc(res)
            if score > best_score:
                best_score, best_digit = score, d

        digits.append(best_digit)

    # 3) reconstroi o número
    number = digits[3]*1000 + digits[2]*100 + digits[1]*10 + digits[0]

    # 4) gera de novo as ROIs “verdadeiras” para apresentação
    _, rois = generate_cistercian_image(
        number, cell_size=CELL_SIZE, margin=MARGIN
    )

    return number, rois, img


def main():
    # 5) lista as imagens dentro de samples/
    folder = "samples"
    imagens = list_images(folder)
    if not imagens:
        print(f"Nenhuma imagem encontrada em `{folder}/`.")
        return

    # 6) escolhe via input
    print("Escolha o índice da imagem para reconhecimento:")
    for i, nome in enumerate(imagens):
        print(f"  [{i}] {nome}")
    idx = int(input("Índice: "))
    arquivo = os.path.join(folder, imagens[idx])

    # 7) reconhece
    numero, rois, original = recognize_image(arquivo)

    # 8) exibe resultado no console
    print(f"\nNúmero reconhecido: {numero}")
    print("Bounding‐boxes dos algarismos:")
    for r in rois:
        print(f"  {r}")

    # e desenha retângulos sobre a imagem
    color = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    for r in rois:
        x1,y1,x2,y2 = r["bbox"]
        cv2.rectangle(color, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imshow(f"Reconhecido: {numero}", color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()