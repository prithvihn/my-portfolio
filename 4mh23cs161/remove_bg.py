import cv2
import numpy as np
from PIL import Image
import os

def remove_background_grabcut(input_path, output_path):
    """
    Remove background using OpenCV's GrabCut algorithm.
    This is a basic approach and may not work well for complex images.
    """
    print(f"Processing image: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return
    
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image at {input_path}")
        return
    
    # Create mask and background/foreground models
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Define rectangle for initial foreground (center region of image)
    h, w = img.shape[:2]
    margin_x = int(w * 0.1)
    margin_y = int(h * 0.05)
    rect = (margin_x, margin_y, w - 2 * margin_x, h - 2 * margin_y)
    
    print("Running GrabCut algorithm... (this may take a moment)")
    # Apply GrabCut
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create binary mask where 0 and 2 are background, 1 and 3 are foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask to image
    img_result = img * mask2[:, :, np.newaxis]
    
    # Convert to RGBA (add alpha channel for transparency)
    img_rgba = cv2.cvtColor(img_result, cv2.COLOR_BGR2BGRA)
    img_rgba[:, :, 3] = mask2 * 255  # Set alpha based on mask
    
    # Save result
    cv2.imwrite(output_path, img_rgba)
    print(f"Successfully saved background-removed image to {output_path}")

if __name__ == "__main__":
    input_path = r"C:/Users/student/.gemini/antigravity/brain/67323652-2d30-4a13-bdcb-d3044fb6e09e/uploaded_media_1769767038338.jpg"
    output_path = "image_no_bg.png"
    
    remove_background_grabcut(input_path, output_path)
