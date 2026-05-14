import time
from controller import ADBController

def capture_screen():
    print("Conectando a ADB para tomar captura...")
    adb = ADBController()
    img_bytes = adb.get_screenshot()
    
    if img_bytes:
        filename = f"screenshot_{int(time.time())}.png"
        with open(filename, "wb") as f:
            f.write(img_bytes)
        print(f"Captura guardada como {filename}")
        print("Recorta los botones de esta imagen y guárdalos en 'bot/templates/' para que el bot los reconozca.")
    else:
        print("Error: No se pudo tomar la captura. Asegúrate de que el emulador esté ejecutándose y ADB esté conectado.")

if __name__ == "__main__":
    capture_screen()
