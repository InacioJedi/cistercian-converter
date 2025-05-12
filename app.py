# app.py
import streamlit as st
import numpy as np
import cv2
from io import BytesIO
import pandas as pd

# --- Função de geração Cisterciana ---
def generate_cistercian_image(number: int, cell_size=40, margin=20):
    """
    Gera imagem em numpy.uint8 (255 fundo, 0 traços) e lista de ROIs.
    """
    if not (1 <= number <= 9999):
        st.error("Número fora do intervalo (1–9999)!")
        return None, None

    # Paths base no quadrante 'unidades' (0)
    base = {
        (0,1):((1,0),(2,0)),
        (0,2):((1,1),(2,1)),
        (0,3):((1,0),(2,1)),
        (0,4):((1,1),(2,0)),
        (0,5):((1,1),(2,0),(1,0)),
        (0,6):((2,0),(2,1)),
        (0,7):((1,0),(2,0),(2,1)),
        (0,8):((1,1),(2,1),(2,0)),
        (0,9):((1,1),(2,1),(2,0),(1,0)),
    }
    # Cria todas as reflexões para dezenas(1), centenas(2), milhares(3)
    d_paths = dict(base)
    for d in range(1,10):
        d_paths[(1,d)] = [(2-x,y)     for x,y in base[(0,d)]]
        d_paths[(2,d)] = [(x,3-y)     for x,y in base[(0,d)]]
        d_paths[(3,d)] = [(2-x,3-y)   for x,y in base[(0,d)]]

    # Canvas
    W = margin*2 + cell_size*3
    H = margin*2 + cell_size*4
    img = np.ones((H,W), dtype=np.uint8)*255

    def to_pix(pt):
        x,y = pt
        return (margin + int(x*cell_size), margin + int(y*cell_size))

    # Haste central
    cv2.line(img, to_pix((1,0)), to_pix((1,3)), 0, 2)

    # Dígitos
    u = number % 10
    t = (number//10)%10
    c = (number//100)%10
    m = (number//1000)%10
    digits = [u,t,c,m]
    names  = ["unidades","dezenas","centenas","milhares"]

    rois = []
    for i,d in enumerate(digits):
        if d==0: continue
        pts = d_paths[(i,d)]
        # Traça cada segmento
        for a,b in zip(pts, pts[1:]):
            cv2.line(img, to_pix(a), to_pix(b), 0, 2)
        # Calcula bbox
        xs = [to_pix(p)[0] for p in pts]
        ys = [to_pix(p)[1] for p in pts]
        rois.append({
            "dígito": d,
            "posição": names[i],
            "bbox": (min(xs),min(ys),max(xs),max(ys))
        })

    return img, rois

# --- Streamlit UI ---
st.title("🔢 Cisterciano ↔ Árabe")
st.sidebar.markdown("## Parâmetros")
n = st.sidebar.number_input("Número (1–9999)", min_value=1, max_value=9999, value=1992, step=1)
if st.sidebar.button("Gerar"):
    img, rois = generate_cistercian_image(n)
    if img is None:
        st.stop()

    # Exibe lado a lado
    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("Número ÁRABE")
        st.write(f"**{n}**")
    with col2:
        st.subheader("CISTERCIANO")
        # Converte numpy para PNG em memória
        is_success, buffer = cv2.imencode(".png", img)
        st.image(buffer.tobytes(), use_column_width=True)

    # Tabela de localização
    st.subheader("📐 Localização dos Algarismos")
    df = pd.DataFrame(rois)
    st.dataframe(df, use_container_width=True)
