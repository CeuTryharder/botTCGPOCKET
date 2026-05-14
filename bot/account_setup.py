"""
account_setup.py - Creación automática de cuenta Google + vinculación TCG Pocket.

ADVERTENCIA: Usar solo para pruebas personales. Puede violar ToS de Google y TCG Pocket.

Flujo:
  1. Abrir Ajustes Android → Cuentas → Añadir cuenta → Google
  2. Completar formulario de registro (nombre, email, contraseña)
  3. Verificar cuenta (o pausar para intervención manual si Google pide teléfono)
  4. Aceptar Términos de Servicio
  5. Guardar credenciales en accounts.csv
  6. Lanzar Pokémon TCG Pocket y hacer Sign In con Google
  7. Completar onboarding del juego
"""

import time
import csv
import random
import string
import os
from datetime import datetime

from controller import ADBController
from vision import Vision

ACCOUNTS_CSV = os.path.join(os.path.dirname(__file__), "accounts.csv")
TCGPOCKET_PACKAGE = "jp.pokemon.pokemontcg"

T_SHORT  = 10
T_MEDIUM = 20
T_LONG   = 60


class AccountSetup:
    def __init__(self, adb: ADBController, vision: Vision):
        self.adb = adb
        self.vision = vision
        self._ensure_csv()

    # ──────────────────────────────────────────
    # Punto de entrada público
    # ──────────────────────────────────────────

    def create_and_link(self) -> bool:
        """
        Flujo completo: genera credenciales → crea cuenta Google →
        vincula con TCG Pocket → guarda en CSV.
        Retorna True si todo salió bien.
        """
        print("\n" + "=" * 55)
        print("  CREACIÓN AUTOMÁTICA DE CUENTA GOOGLE + TCG POCKET")
        print("=" * 55)

        creds = self._generate_credentials()
        print(f"\n[*] Credenciales generadas:")
        print(f"    Nombre   : {creds['first_name']} {creds['last_name']}")
        print(f"    Email    : {creds['email']}")
        print(f"    Password : {creds['password']}")

        print("\n[PASO 1/3] Creando cuenta Google...")
        if not self._create_google_account(creds):
            print("[ERROR] No se pudo crear la cuenta Google. Proceso abortado.")
            return False

        print("\n[PASO 2/3] Vinculando con Pokémon TCG Pocket...")
        if not self._link_tcg_pocket(creds):
            print("[ERROR] No se pudo vincular con TCG Pocket.")
            creds["status"] = "google_only"
            self._save_credentials(creds)
            return False

        print("\n[PASO 3/3] Guardando credenciales...")
        creds["status"] = "linked"
        self._save_credentials(creds)

        print("\n[OK] Proceso completado. Credenciales en:", ACCOUNTS_CSV)
        return True

    # ──────────────────────────────────────────
    # Generación de credenciales
    # ──────────────────────────────────────────

    def _generate_credentials(self) -> dict:
        first_names = ["Alex","Jordan","Morgan","Taylor","Casey","Riley","Avery","Quinn","Drew","Blake"]
        last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Moore"]
        first = random.choice(first_names)
        last  = random.choice(last_names)
        suffix = "".join(random.choices(string.digits, k=5))
        email  = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"
        password = (
            random.choice(string.ascii_uppercase)
            + "".join(random.choices(string.ascii_lowercase, k=7))
            + random.choice(string.digits)
            + random.choice("!@#$%")
        )
        return {
            "first_name"  : first,
            "last_name"   : last,
            "email"       : email,
            "password"    : password,
            "birth_day"   : random.randint(1, 28),
            "birth_month" : random.randint(1, 12),
            "birth_year"  : random.randint(1985, 2000),
            "created_at"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status"      : "pending",
        }

    # ──────────────────────────────────────────
    # Flujo de creación de cuenta Google
    # ──────────────────────────────────────────

    def _create_google_account(self, creds: dict) -> bool:
        # A. Abrir Ajustes → Cuentas
        print("  [A] Abriendo Ajustes de Android...")
        self.adb.press_key("HOME")
        time.sleep(1)
        self.adb.launch_app("com.android.settings")
        time.sleep(2)

        if not self._wc("settings_accounts.png", T_MEDIUM):
            print("  [!] Template no encontrado; lanzando AccountSettings directamente...")
            self.adb.launch_activity("com.android.settings", ".accounts.AccountSettings")
            time.sleep(2)

        # B. Añadir cuenta
        print("  [B] Tocando 'Añadir cuenta'...")
        if not self._wc("add_account_btn.png", T_SHORT):
            return False
        time.sleep(1)

        # C. Seleccionar Google
        print("  [C] Seleccionando Google...")
        if not self._wc("google_account_btn.png", T_SHORT):
            return False
        time.sleep(2)

        # D. Crear cuenta
        print("  [D] Tocando 'Crear cuenta'...")
        if not self._wc("create_account_btn.png", T_MEDIUM):
            return False
        time.sleep(1)
        self._wc("for_myself_btn.png", timeout=5)   # opcional
        time.sleep(1)

        # E. Nombre y apellido
        print(f"  [E] Nombre: {creds['first_name']} / Apellido: {creds['last_name']}")
        if self._wc("first_name_field.png", T_SHORT):
            self.adb.clear_text_field()
            self.adb.type_text(creds["first_name"])
        if self._wc("last_name_field.png", T_SHORT):
            self.adb.clear_text_field()
            self.adb.type_text(creds["last_name"])
        self._tap_next()
        time.sleep(1)

        # F. Fecha de nacimiento
        print(f"  [F] Fecha de nacimiento: {creds['birth_day']}/{creds['birth_month']}/{creds['birth_year']}")
        self._fill_birthdate(creds)
        self._tap_next()
        time.sleep(1)

        # G. Email
        print(f"  [G] Email: {creds['email']}")
        self._wc("create_own_email_btn.png", timeout=5)
        time.sleep(0.5)
        if self._wc("email_field.png", T_SHORT):
            self.adb.clear_text_field()
            self.adb.type_text(creds["email"].replace("@gmail.com", ""))
        self._tap_next()
        time.sleep(2)

        # H. Contraseña
        print("  [H] Contraseña...")
        if self._wc("password_field.png", T_SHORT):
            self.adb.clear_text_field()
            self.adb.type_text(creds["password"])
        if self._wc("confirm_password_field.png", timeout=5):
            self.adb.clear_text_field()
            self.adb.type_text(creds["password"])
        self._tap_next()
        time.sleep(2)

        # I. Verificación por teléfono (puede requerir intervención manual)
        print("  [I] Comprobando verificación por teléfono...")
        if self._is_phone_screen():
            print()
            print("  ⚠️  ACCIÓN MANUAL REQUERIDA")
            print("  ─────────────────────────────────────────────")
            print("  Google está pidiendo verificación por teléfono.")
            print("  Introduce el número manualmente en el emulador.")
            print("  El bot intentará omitirlo; si no puede, esperará 120s.")
            print("  ─────────────────────────────────────────────")
            if not self._try_skip_phone():
                if not self._wc("agree_btn.png", timeout=120):
                    print("  [ERROR] Timeout en verificación de teléfono.")
                    return False

        # J. Saltar pantallas opcionales
        for tmpl in ["skip_btn.png", "not_now_btn.png"]:
            self._wc(tmpl, timeout=5)
            time.sleep(0.5)

        # K. Aceptar ToS
        print("  [K] Aceptando Términos de Servicio...")
        if not self._wc("agree_btn.png", T_MEDIUM):
            self._wc("accept_btn.png", T_SHORT)
        time.sleep(2)

        # L. Pantallas post-registro
        self._wc("skip_btn.png",   timeout=10)
        self._wc("not_now_btn.png", timeout=5)
        time.sleep(1)

        print("  [OK] Cuenta Google creada.")
        return True

    # ──────────────────────────────────────────
    # Flujo de vinculación con TCG Pocket
    # ──────────────────────────────────────────

    def _link_tcg_pocket(self, creds: dict) -> bool:
        print("  [A] Volviendo a Home...")
        self.adb.press_key("HOME")
        time.sleep(1)

        print(f"  [B] Lanzando TCG Pocket ({TCGPOCKET_PACKAGE})...")
        self.adb.launch_app(TCGPOCKET_PACKAGE)
        time.sleep(5)

        # Esperar pantalla de inicio del juego
        print("  [C] Esperando pantalla de inicio...")
        if not self._wc("tcgp_logo.png", T_LONG):
            print("  [!] No apareció la pantalla de inicio. ¿Está instalado el juego?")
            return False
        time.sleep(2)

        # Login con Google
        print("  [D] Tocando 'Sign in with Google'...")
        if not self._wc("sign_in_google.png", T_MEDIUM):
            return False
        time.sleep(2)

        # Selector de cuenta
        print("  [E] Seleccionando cuenta...")
        if self._wc("select_account.png", T_SHORT):
            time.sleep(1)
            if not self._tap_account_item():
                self.adb.tap(540, 600)   # fallback: primer item aprox.
            time.sleep(2)

        # Onboarding del juego
        print("  [F] Completando onboarding...")
        self._complete_onboarding(creds)

        print("  [OK] Cuenta vinculada con TCG Pocket.")
        return True

    def _complete_onboarding(self, creds: dict):
        # Aceptar términos del juego
        for tmpl in ["agree_btn.png", "accept_btn.png", "tcgp_terms_accept.png"]:
            self._wc(tmpl, timeout=8)
            time.sleep(0.5)

        # Edad si la pide
        if self._wc("age_field.png", timeout=5):
            self.adb.type_text(str(creds["birth_year"]))
            self._tap_next()
            time.sleep(1)

        # Nombre de entrenador
        print("  [F.1] Nombre de entrenador...")
        if self._wc("trainer_name_field.png", T_MEDIUM):
            self.adb.clear_text_field()
            self.adb.type_text(creds["first_name"][:12])
            time.sleep(0.5)
            self._wc("confirm_trainer_btn.png", T_SHORT)
            time.sleep(1)

        # Skip tutoriales
        for _ in range(10):
            screenshot = self.adb.get_screenshot()
            if not screenshot:
                break
            found = False
            for tmpl in ["skip_btn.png", "ok_btn.png", "next_btn.png", "not_now_btn.png"]:
                if self.vision.find_template_on_screen(screenshot, tmpl):
                    self._wc(tmpl, timeout=5)
                    time.sleep(1)
                    found = True
                    break
            if not found:
                time.sleep(2)

    # ──────────────────────────────────────────
    # Helpers de UI
    # ──────────────────────────────────────────

    def _wc(self, template: str, timeout: int = 10, delay: float = 1.0) -> bool:
        """wait_and_click shorthand."""
        start = time.time()
        while time.time() - start < timeout:
            shot = self.adb.get_screenshot()
            if not shot:
                time.sleep(delay)
                continue
            loc = self.vision.find_template_on_screen(shot, template)
            if loc:
                print(f"    → [{template}] en {loc}")
                self.adb.tap(loc[0], loc[1])
                return True
            time.sleep(delay)
        print(f"    → [{template}] no encontrado (timeout {timeout}s)")
        return False

    def _tap_next(self):
        if not self._wc("next_btn_google.png", timeout=5):
            self.adb.press_key("ENTER")
        time.sleep(0.5)

    def _fill_birthdate(self, creds: dict):
        for field_tmpl, value in [
            ("birthdate_day_field.png",   str(creds["birth_day"])),
            ("birthdate_month_field.png", str(creds["birth_month"])),
            ("birthdate_year_field.png",  str(creds["birth_year"])),
        ]:
            if self._wc(field_tmpl, timeout=5):
                self.adb.type_text(value)
                self.adb.press_key("TAB")

    def _is_phone_screen(self) -> bool:
        shot = self.adb.get_screenshot()
        return bool(shot and self.vision.find_template_on_screen(shot, "phone_verify_screen.png"))

    def _try_skip_phone(self) -> bool:
        for tmpl in ["skip_phone_btn.png", "not_now_btn.png", "skip_btn.png"]:
            if self._wc(tmpl, timeout=5):
                print("  [OK] Verificación por teléfono omitida.")
                return True
        return False

    def _tap_account_item(self) -> bool:
        shot = self.adb.get_screenshot()
        if not shot:
            return False
        loc = self.vision.find_template_on_screen(shot, "google_account_item.png")
        if loc:
            self.adb.tap(loc[0], loc[1])
            return True
        return False

    # ──────────────────────────────────────────
    # Persistencia
    # ──────────────────────────────────────────

    def _ensure_csv(self):
        if not os.path.exists(ACCOUNTS_CSV):
            with open(ACCOUNTS_CSV, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=[
                    "email","password","first_name","last_name","created_at","status"
                ]).writeheader()

    def _save_credentials(self, creds: dict):
        with open(ACCOUNTS_CSV, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=[
                "email","password","first_name","last_name","created_at","status"
            ]).writerow({k: creds[k] for k in ["email","password","first_name","last_name","created_at","status"]})
        print(f"  ✓ Guardado: {creds['email']} [{creds['status']}]")

    def list_accounts(self):
        """Muestra en consola todas las cuentas guardadas."""
        if not os.path.exists(ACCOUNTS_CSV):
            print("No hay cuentas guardadas todavía.")
            return
        with open(ACCOUNTS_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            print("El fichero accounts.csv está vacío.")
            return
        print(f"\n{'Email':<40} {'Status':<15} {'Creada el'}")
        print("─" * 75)
        for r in rows:
            print(f"{r['email']:<40} {r['status']:<15} {r['created_at']}")
        print(f"\nTotal: {len(rows)} cuenta(s)")
