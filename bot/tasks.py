import time
from controller import ADBController
from vision import Vision

class BotTasks:
    def __init__(self, adb: ADBController, vision: Vision):
        self.adb = adb
        self.vision = vision

    def _wait_and_click(self, template_name, timeout=10, delay=1, click_offset_y=0):
        print(f"Buscando '{template_name}' en la pantalla...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            screenshot = self.adb.get_screenshot()
            if not screenshot:
                time.sleep(delay)
                continue
                
            loc = self.vision.find_template_on_screen(screenshot, template_name)
            if loc:
                print(f"¡Encontrado! Habilitando clic en {loc}")
                self.adb.tap(loc[0], loc[1] + click_offset_y)
                return True
            time.sleep(delay)
            
        print(f"Tiempo agotado (timeout) esperando {template_name}.")
        return False

    def farm_solo_battle(self):
        """
        Lógica para farmear batallas en solitario usando imágenes base.
        """
        print("Iniciando rutina de farmeo de batallas en solitario...")
        print("Asegúrate de estar en la pantalla de selección de batalla.")
        
        battles_completed = 0
        while True:
            print(f"\n--- Iniciando Batalla #{battles_completed + 1} ---")
            
            # Paso 1: Clic en el botón para iniciar la batalla
            if not self._wait_and_click("battle_btn.png", timeout=5):
                print("No se encontró el botón de batalla. Deteniendo bot.")
                break
                
            # Paso 2: Activar auto-batalla si está disponible (opcional, intenta durante un tiempo pero no interrumpe si falla)
            self._wait_and_click("auto_battle_btn.png", timeout=15)
            
            # Paso 3: Esperar que termine la batalla buscando botones de victoria, derrota o "ok"
            print("Esperando a que termine la batalla...")
            while True:
                screenshot = self.adb.get_screenshot()
                if not screenshot:
                    time.sleep(2)
                    continue
                    
                # Comprobar si aparecen botones de "ok", "siguiente", o "continuar"
                if self.vision.find_template_on_screen(screenshot, "ok_btn.png"):
                    self._wait_and_click("ok_btn.png", timeout=5)
                    break
                elif self.vision.find_template_on_screen(screenshot, "next_btn.png"):
                    self._wait_and_click("next_btn.png", timeout=5)
                    break
                    
                time.sleep(3) # Esperar un rato antes de volver a verificar el estado de la batalla
                
            battles_completed += 1
            print(f"Batalla #{battles_completed} completada. Regresando al menú...")
            time.sleep(3)

    def claim_missions(self):
        """
        Lógica para navegar a la pestaña de misiones y reclamar recompensas.
        """
        print("Iniciando rutina de reclamar misiones...")
        if self._wait_and_click("missions_tab.png", timeout=5):
            time.sleep(1)
            self._wait_and_click("claim_all_btn.png", timeout=5)
            time.sleep(2)
            self._wait_and_click("ok_btn.png", timeout=5)
            print("Recompensas de misiones reclamadas con éxito.")
        else:
            print("No se pudo encontrar la pestaña de misiones.")

    def link_google_account(self, account_setup) -> bool:
        """
        Crea una cuenta Google nueva y la vincula automáticamente con
        Pokémon TCG Pocket. Delega la lógica completa en AccountSetup.

        Args:
            account_setup: Instancia de AccountSetup inicializada.

        Returns:
            True si el proceso completó con éxito, False si falló.
        """
        print("Iniciando creación y vinculación de cuenta Google...")
        return account_setup.create_and_link()
