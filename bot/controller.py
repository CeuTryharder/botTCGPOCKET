import subprocess
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
