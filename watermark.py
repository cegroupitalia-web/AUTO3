import os
from PIL import Image

def aggiungi_watermark():
    input_folder = 'AUTO3'
    output_folder = 'AUTO3_PRONTE'
    watermark_path = 'watermark.png'

    if not os.path.exists(watermark_path):
        print("Errore: watermark.png non trovato!")
        return

    wm = Image.open(watermark_path).convert("RGBA")

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Percorsi
                rel_path = os.path.relpath(root, input_folder)
                target_dir = os.path.join(output_folder, rel_path)
                os.makedirs(target_dir, exist_ok=True)

                img_path = os.path.join(root, file)
                out_path = os.path.join(target_dir, file)

                # Elaborazione
                with Image.open(img_path).convert("RGBA") as base:
                    # Ridimensiona watermark al 15% della larghezza foto
                    w_width = int(base.width * 0.15)
                    w_height = int(wm.height * (w_width / wm.width))
                    wm_resized = wm.resize((w_width, w_height))

                    # Incolla in basso a destra
                    base.paste(wm_resized, (base.width - w_width - 20, base.height - w_height - 20), wm_resized)
                    base.convert("RGB").save(out_path, "JPEG", quality=90)
                print(f"Fatto: {file}")

if __name__ == "__main__":
    aggiungi_watermark()
