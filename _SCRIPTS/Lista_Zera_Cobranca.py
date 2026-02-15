import pyautogui
import time

# Definindo a quantidade de repetições
repeticoes = 80

# Aguarda alguns segundos antes de começar para que você possa preparar o ambiente
time.sleep(5)

# Loop para simular os pressionamentos de teclas
for _ in range(repeticoes):
    pyautogui.press('tab', presses=4)  # Pressiona a tecla "Tab" 4 vezes
    pyautogui.press('0')  # Pressiona a tecla "0"
    pyautogui.press('enter')  # Pressiona a tecla "Enter" (se necessário)
