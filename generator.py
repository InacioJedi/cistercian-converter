import numpy as np
import cv2

def generate_cistercian_image(number: int, cell_size: int = 40, margin: int = 20):
    """
    Gera a representação cisterciense de um número de 1 a 9999.
    Retorna:
        img: numpy.ndarray (uint8) com 255 fundo branco e traços em preto.
        rois: list de dicts com chaves 'dígito', 'posição' e 'bbox' (x1, y1, x2, y2).
    """
    if number < 1 or number > 9999:
        raise ValueError("Número fora do intervalo suportado (1-9999)")

    # Paths base para o quadrante unidades (pos=0)
    base_paths = {
        (0, 1): ((1, 0), (2, 0)),
        (0, 2): ((1, 1), (2, 1)),
        (0, 3): ((1, 0), (2, 1)),
        (0, 4): ((1, 1), (2, 0)),
        (0, 5): ((1, 1), (2, 0), (1, 0)),
        (0, 6): ((2, 0), (2, 1)),
        (0, 7): ((1, 0), (2, 0), (2, 1)),
        (0, 8): ((1, 1), (2, 1), (2, 0)),
        (0, 9): ((1, 1), (2, 1), (2, 0), (1, 0)),
    }

    # Geração dos paths para dezenas(pos=1), centenas(pos=2), milhares(pos=3) por reflexão
    d_paths = dict(base_paths)
    for d in range(1, 10):
        d_paths[(1, d)] = [(2 - x, y) for x, y in base_paths[(0, d)]]
        d_paths[(2, d)] = [(x, 3 - y) for x, y in base_paths[(0, d)]]
        d_paths[(3, d)] = [(2 - x, 3 - y) for x, y in base_paths[(0, d)]]

    # Cria canvas
    width = margin * 2 + cell_size * 3
    height = margin * 2 + cell_size * 4
    img = np.ones((height, width), dtype=np.uint8) * 255

    def to_pix(pt):
        """Converte coordenadas de grade (x, y) em pixels (col, lin)"""
        x, y = pt
        return (margin + int(x * cell_size), margin + int(y * cell_size))

    # Desenha a haste central
    cv2.line(img, to_pix((1, 0)), to_pix((1, 3)), color=0, thickness=2)

    # Decompõe dígitos
    unidades = number % 10
    dezenas = (number // 10) % 10
    centenas = (number // 100) % 10
    milhares = (number // 1000) % 10
    digits = [unidades, dezenas, centenas, milhares]
    positions = ['unidades', 'dezenas', 'centenas', 'milhares']

    rois = []
    for pos, digit in enumerate(digits):
        if digit == 0:
            continue
        pts = d_paths[(pos, digit)]
        # Desenha cada segmento como linha entre pontos consecutivos
        for i in range(len(pts) - 1):
            cv2.line(img, to_pix(pts[i]), to_pix(pts[i + 1]), color=0, thickness=2)

        # Calcula bounding box
        xs = [to_pix(p)[0] for p in pts]
        ys = [to_pix(p)[1] for p in pts]
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        rois.append({
            'dígito': digit,
            'posição': positions[pos],
            'bbox': (x1, y1, x2, y2)
        })

    return img, rois