Cistercian Numeral Converter

Este projeto permite gerar e reconhecer numerais cistercienses de números arábicos (1–9999).

Estrutura do Projeto

├── .venv/                # Virtual environment
├── samples/              # Imagens cistercienses de teste (geradas automaticamente)
├── generator.py          # Função de geração de imagem + ROIs
├── generate_samples.py   # Script para popular samples/ com imagens de exemplo
├── recognize.py          # Reconhecimento de número a partir de imagem
├── app.py                # Frontend Streamlit (gera e reconhece via Web UI)
├── utils.py              # Utilitários (opcional)
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo

Pré‑requisitos

Python 3.7+ instalado no sistema

pip (gerenciador de pacotes)

virtualenv (recomendado para isolar dependências)

Instalação e Configuração

Clone o repositório:

git clone <URL_DO_REPOSITÓRIO>
cd <NOME_DO_PROJETO>

Crie e ative o virtualenv:

Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate

Atualize o pip e instale dependências:

pip install --upgrade pip
pip install streamlit opencv-python numpy pandas matplotlib

Ambiente headless (servidor): use opencv-python-headless em vez de opencv-python:

pip install streamlit opencv-python-headless numpy pandas matplotlib

(Opcional) Gere o requirements.txt:

pip freeze > requirements.txt

Gerando Imagens de Teste

Use o script generate_samples.py para popular a pasta samples/:

python generate_samples.py

Este comando gerará arquivos como:

 samples/1.png
 samples/5.png
 samples/10.png
 samples/42.png
 samples/1992.png
 samples/2023.png
 samples/9999.png

Para gerar números personalizados, passe-os como argumentos:

python generate_samples.py 314 159 26

Interface Web (Streamlit)

Execute o frontend via Streamlit para gerar e reconhecer diretamente no navegador:

streamlit run app.py
# ou
python -m streamlit run app.py

No navegador, a aplicação oferecerá:

Geração: insira um número (1–9999) e visualize o numeral cisterciense ao lado do arábico.

Reconhecimento: selecione uma imagem de samples/ e veja o número reconhecido + bounding‑boxes.

Reconhecimento via CLI

Para reconhecer imagens via linha de comando:

python recognize.py

Siga o prompt:

Escolha o índice da imagem em samples/.

O script imprimirá no console:

Número reconhecido

Lista de bounding‑boxes

Será aberta uma janela (OpenCV) com a imagem destacada.

Se estiver usando opencv-python-headless, substitua o bloco cv2.imshow(...) no final de recognize.py por um snippet Matplotlib:

import matplotlib.pyplot as plt
plt.imshow(color[:, :, ::-1])  # BGR → RGB
plt.axis('off')
plt.show()

Módulos Principais

generator.py: define generate_cistercian_image(number, cell_size, margin) → retorna (img, rois).

generate_samples.py: usa generator.py para criar imagens em samples/.

recognize.py: importa generate_cistercian_image para fazer template‑matching e reconhecer números.

app.py: frontend com Streamlit (gera e reconhece em Web UI).

utils.py: funções auxiliares (opcional).

