import pyautogui, webbrowser
from time import sleep

webbrowser.open("https://web.whatsapp.com/send?phone=+573135993691")
sleep(50)
for i in range(100000):
    pyautogui.typewrite("Falco")
    pyautogui.press("enter")
    sleep(1)

    pyautogui.typewrite("¿Sientes el terror? XD")
    sleep(1)
    pyautogui.press("enter")
  