import io
import os

from PIL import Image

for file in os.listdir("seeds/images"):
    if file.endswith((".avif", ".jpg", ".jpeg", ".png", ".webp")):
        img_path = os.path.join("seeds/images", file)
        webp_path = img_path.rsplit(".", 1)[0] + ".webp"
        img = Image.open(img_path)

        w, h = img.size

        if w > 400:
            new_w = 400
            new_h = int((new_w / w) * h)
            img = img.resize((new_w, new_h))

        # Maybe same flietype
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=80)

        os.remove(img_path)

        with open(webp_path, "wb") as f:
            f.write(buf.getbuffer())

        print(f"Converted {file} to {os.path.basename(webp_path)}")
