import subprocess
import re
import time

class ADBController:
    def __init__(self, device_id=None):
        self.device_id = device_id
        
    def _run_adb_cmd(self, args):
        cmd = ["adb"]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"ADB command failed: {e}")
            return None

    def tap(self, x, y):
        """Tap at the specified (x, y) coordinates."""
        print(f"Tapping on ({x}, {y})")
        self._run_adb_cmd(["shell", "input", "tap", str(x), str(y)])
        
    def swipe(self, x1, y1, x2, y2, duration_ms=500):
        """Swipe from (x1, y1) to (x2, y2)."""
        print(f"Swiping from ({x1}, {y1}) to ({x2}, {y2}) over {duration_ms}ms")
        self._run_adb_cmd(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)])

    def get_screenshot(self) -> bytes:
        """Capture the screen in raw PNG format."""
        cmd = ["adb"]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(["exec-out", "screencap", "-p"])

        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"ADB screenshot failed: {e}")
            return b""

    def type_text(self, text: str):
        """Type text into the currently focused field via ADB input."""
        # Escape special shell characters for ADB input text
        escaped = text.replace(" ", "%s").replace("'", "\'").replace("&", "\&")
        print(f"Typing: {text}")
        self._run_adb_cmd(["shell", "input", "text", escaped])

    def press_key(self, keycode: str):
        """
        Send an Android keycode via ADB.
        Common values: HOME, BACK, ENTER, TAB, DEL
        Full list: https://developer.android.com/reference/android/view/KeyEvent
        """
        keycode_map = {
            "HOME" : "KEYCODE_HOME",
            "BACK" : "KEYCODE_BACK",
            "ENTER": "KEYCODE_ENTER",
            "TAB"  : "KEYCODE_TAB",
            "DEL"  : "KEYCODE_DEL",
        }
        adb_key = keycode_map.get(keycode.upper(), keycode)
        print(f"Pressing key: {adb_key}")
        self._run_adb_cmd(["shell", "input", "keyevent", adb_key])

    def launch_app(self, package_name: str):
        """Launch an Android app by its package name using a monkey intent."""
        print(f"Launching app: {package_name}")
        self._run_adb_cmd([
            "shell", "monkey", "-p", package_name,
            "-c", "android.intent.category.LAUNCHER", "1"
        ])

    def launch_activity(self, package_name: str, activity: str):
        """Launch a specific Activity inside a package."""
        component = f"{package_name}/{activity}"
        print(f"Launching activity: {component}")
        self._run_adb_cmd(["shell", "am", "start", "-n", component])

    def clear_text_field(self):
        """
        Clear the currently focused text field by selecting all text
        and deleting it.
        """
        # Select all → delete
        self._run_adb_cmd(["shell", "input", "keyevent", "KEYCODE_CTRL_A"])
        time.sleep(0.1)
        self._run_adb_cmd(["shell", "input", "keyevent", "KEYCODE_DEL"])

    def get_device_resolution(self) -> tuple:
        """
        Returns the screen resolution as (width, height).
        Useful for adapting coordinates to different screen sizes.
        """
        output = self._run_adb_cmd(["shell", "wm", "size"])
        if output:
            match = re.search(r"(\d+)x(\d+)", output)
            if match:
                return int(match.group(1)), int(match.group(2))
        return (1080, 1920)  # fallback resolution
