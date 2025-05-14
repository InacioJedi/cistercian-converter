Cistercian Numeral Converter

Este projeto permite gerar e reconhecer numerais cistercienses a partir de números arábicos (1–9999).

📂 Estrutura do Projeto

├── .venv/                 # Ambiente virtual
├── samples/               # Imagens de teste geradas automaticamente
├── generator.py           # Geração de imagem e definição de ROIs
├── generate_samples.py    # Script para popular a pasta samples/
├── recognize.py           # Reconhecimento de numerais em imagens
├── app.py                 # Frontend Streamlit (Geração e Reconhecimento via Web)
├── utils.py               # Funções auxiliares (opcional)
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo

🚀 Pré‑requisitos

Python 3.7+

pip (gerenciador de pacotes)

virtualenv (recomendado)

💻 Instalação

Clone o repositório:

git clone <URL_DO_REPOSITÓRIO>
cd <NOME_DO_PROJETO>

2. **Crie e ative o ambiente virtual**
   - **Windows (PowerShell)**
python -m venv .venv
.venv\Scripts\Activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate


3. **Atualize o pip e instale as dependências**
   ```bash
pip install --upgrade pip
pip install -r requirements.txt

Caso execute em servidor/headless, substitua opencv-python por opencv-python-headless no requirements.txt.

🎨 Gerando Imagens de Teste

Para popular a pasta samples/ com numerais cistercienses:

python generate_samples.py

Isso criará arquivos como:

samples/1.png
samples/42.png
samples/1992.png
... e assim por diante.

Para números específicos:

python generate_samples.py 314 159 26

🌐 Interface Web (Streamlit)

Execute o frontend para gerar e reconhecer numerais via navegador:

streamlit run app.py
# ou
python -m streamlit run app.py

Funcionalidades

Geração: Insira um número (1–9999) e visualize o numeral cisterciense.

Reconhecimento: Selecione uma imagem de samples/ para obter o valor arábico e as caixas delimitadoras (ROIs).

🔍 Reconhecimento via CLI

python recognize.py

Escolha o índice da imagem em samples/.

O script exibirá no console:

Número reconhecido

Lista de bounding boxes (ROIs)

Será aberta uma janela (OpenCV) com a imagem destacada.

Dica: Se usar opencv-python-headless, substitua o bloco cv2.imshow(...) por:

import matplotlib.pyplot as plt
plt.imshow(color[:, :, ::-1])  # BGR → RGB
plt.axis('off')
plt.show()

🛠️ Módulos Principais

generator.py: Define generate_cistercian_image(number, cell_size, margin) → (img, rois)

generate_samples.py: Popula samples/ chamando generator.py

recognize.py: Realiza template matching para reconhecer números

app.py: Frontend em Streamlit

utils.py: Funções utilitárias (configuração, logging, etc.)
