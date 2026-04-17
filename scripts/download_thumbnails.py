import csv
import re
import urllib.request
import os

try:
    from PIL import Image, ImageChops
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
csv_path = os.path.join(project_dir, 'videos.csv')
thumbnails_dir = os.path.join(project_dir, 'thumbnails')

def get_yt_id(url):
    if not url: return None
    match = re.search(r'(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=|shorts\/))([^"&?\/\s]{11})', url)
    return match.group(1) if match else None

def auto_crop(image_path, threshold=15):
    if not HAS_PILLOW:
        return
    try:
        with Image.open(image_path) as img:
            img_rgb = img.convert("RGB")
            bg = Image.new("RGB", img_rgb.size, (0, 0, 0))
            diff = ImageChops.difference(img_rgb, bg)
            diff = ImageChops.add(diff, diff, 2.0, -threshold)
            bbox = diff.getbbox()
            if bbox:
                width, height = img_rgb.size
                c_left, c_upper, c_right, c_lower = bbox
                if c_left > 5 or c_upper > 5 or (width - c_right) > 5 or (height - c_lower) > 5:
                    print(f"Cropping {os.path.basename(image_path)} from {img_rgb.size} to {bbox}")
                    cropped = img.crop(bbox)
                    cropped.save(image_path)
    except Exception as e:
        print(f"Failed to crop {image_path}: {e}")

os.makedirs(thumbnails_dir, exist_ok=True)

rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    if 'Thumbnail' not in header:
        header.append('Thumbnail')
    
    for row in reader:
        # Pad row to match header length
        while len(row) < len(header) - 1:
            row.append('')
            
        link = row[2]
        yt_id = get_yt_id(link)
        thumbnail_path = ''
        if yt_id:
            thumbnail_rel_path = f'thumbnails/{yt_id}.jpg'
            thumbnail_full_path = os.path.join(project_dir, thumbnail_rel_path)
            
            if not os.path.exists(thumbnail_full_path):
                try:
                    urllib.request.urlretrieve(f'https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg', thumbnail_full_path)
                    auto_crop(thumbnail_full_path)
                except:
                    try:
                        urllib.request.urlretrieve(f'https://img.youtube.com/vi/{yt_id}/hqdefault.jpg', thumbnail_full_path)
                        auto_crop(thumbnail_full_path)
                    except Exception as e:
                        print(f"Failed to download for {yt_id}: {e}")
                        thumbnail_rel_path = ''
            
            thumbnail_path = thumbnail_rel_path if yt_id else ''
        
        if len(row) == len(header) - 1:
            row.append(thumbnail_path)
        else:
            row[header.index('Thumbnail')] = thumbnail_path
        rows.append(row)

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Thumbnails downloaded and CSV updated.")
