import cv2
import numpy as np
from typing import Tuple, Optional

class Vision:
    def __init__(self, template_folder="templates"):
        self.template_folder = template_folder

    def find_template_on_screen(self, screen_image_bytes: bytes, template_filename: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Searches for a template image inside the full screen image.
        Returns the (x, y) center coordinates of the match if found, else None.
        """
        # Convert bytes to numpy array then to cv2 image
        np_arr = np.frombuffer(screen_image_bytes, np.uint8)
        screen_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if screen_img is None:
            return None

        # Load the template image
        template_path = f"{self.template_folder}/{template_filename}"
        template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)

        if template_img is None:
            print(f"Failed to load template: {template_path}")
            return None

        # Perform template matching
        result = cv2.matchTemplate(screen_img, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # Calculate the center of the matched region
            h, w = template_img.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        
        return None
