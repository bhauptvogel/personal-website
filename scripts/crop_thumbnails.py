from PIL import Image, ImageChops
import os
import glob

def auto_crop(image_path, threshold=15):
    with Image.open(image_path) as img:
        # Convert to RGB to ensure uniform processing
        img = img.convert("RGB")
        
        # Create a background image to difference against
        bg = Image.new("RGB", img.size, (0, 0, 0))
        diff = ImageChops.difference(img, bg)
        
        # Apply a threshold to ignore compression artifacts
        diff = ImageChops.add(diff, diff, 2.0, -threshold)
        
        bbox = diff.getbbox()
        if bbox:
            # Check if crop is substantial (i.e. not just 1-2 pixels)
            width, height = img.size
            c_left, c_upper, c_right, c_lower = bbox
            if c_left > 5 or c_upper > 5 or (width - c_right) > 5 or (height - c_lower) > 5:
                print(f"Cropping {os.path.basename(image_path)} from {img.size} to {bbox}")
                cropped = img.crop(bbox)
                cropped.save(image_path)
            else:
                print(f"Skipping {os.path.basename(image_path)}, no significant black borders.")
        else:
            print(f"Skipping {os.path.basename(image_path)}, empty or completely black.")

thumbnail_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'thumbnails')

for img_path in glob.glob(os.path.join(thumbnail_dir, '*.jpg')):
    auto_crop(img_path)
