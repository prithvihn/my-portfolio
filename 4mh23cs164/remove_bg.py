import cv2
import numpy as np
from PIL import Image
import sys
import os

def remove_background_grabcut(input_path, output_path):
    """
    Remove background using GrabCut algorithm.
    Works best when the subject is centered in the image.
    """
    print(f"Processing {input_path}...")
    
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image from {input_path}")
        return
    
    # Create mask
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # Rectangle for initial detection (assumes subject fills most of center)
    h, w = img.shape[:2]
    margin_x = int(w * 0.05)
    margin_y = int(h * 0.02)
    rect = (margin_x, margin_y, w - 2*margin_x, h - 2*margin_y)
    
    # Models for GrabCut
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Apply GrabCut
    print("Applying GrabCut algorithm (this may take a moment)...")
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create binary mask
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask to get transparent background
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask2 * 255
    
    # Save result
    cv2.imwrite(output_path, result)
    print(f"Success! Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_bg.py <input_image_path> <output_image_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    remove_background_grabcut(input_path, output_path)
