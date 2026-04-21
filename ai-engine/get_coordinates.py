import cv2
import numpy as np

# Lista para armazenar os pontos clicados
points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Ponto capturado: [{x}, {y}]")
        points.append([x, y])
        # Desenha um círculo no local do clique para referência visual
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Capturador de Coordenadas", img)

# 0 para webcam ou a URL da sua câmera IP
cap = cv2.VideoCapture(0)
ret, img = cap.read()

if not ret:
    print("Erro ao abrir a câmera")
    exit()

cv2.imshow("Capturador de Coordenadas", img)
cv2.setMouseCallback("Capturador de Coordenadas", click_event)

print("INSTRUÇÕES:")
print("1. Clique nos 4 cantos de um móvel (em ordem: superior-esq, superior-dir, inferior-dir, inferior-esq)")
print("2. Pressione 'q' para finalizar e gerar o código.")

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

# Formata a saída para o seu main.py
if len(points) >= 4:
    print("\n--- COPIE O CÓDIGO ABAIXO PARA O SEU main.py ---")
    # Agrupa de 4 em 4 pontos caso você tenha clicado em vários móveis
    for i in range(0, len(points), 4):
        grupo = points[i:i+4]
        if len(grupo) == 4:
            print(f"np.array({grupo})")
    print("--------------------------------------------------")
else:
    print("Você capturou menos de 4 pontos.")
