from rembg import remove
from PIL import Image
import io

def remove_background(input_path, output_path):
    print(f"Processing {input_path}...")
    try:
        with open(input_path, 'rb') as i:
            input_image = i.read()
        
        output_image = remove(input_image)
        
        with open(output_path, 'wb') as o:
            o.write(output_image)
            
        print(f"Background removed successfully! Saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "Bottle.jpeg"
    output_file = "bottle_nobg.png"
    remove_background(input_file, output_file)
