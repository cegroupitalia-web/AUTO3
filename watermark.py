import os
from PIL import Image

def aggiungi_watermark():
    # Usiamo percorsi assoluti per essere sicuri al 100%
    base_path = os.getcwd()
    input_folder = os.path.join(base_path, 'AUTO3')
    output_folder = os.path.join(base_path, 'AUTO3_PRONTE')
    watermark_path = os.path.join(base_path, 'watermark.png')

    if not os.path.exists(watermark_path):
        print(f"ERRORE: Il file {watermark_path} non esiste!")
        return

    wm = Image.open(watermark_path).convert("RGBA")
    count = 0

    # Scansiona tutto
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Controllo estensioni (accetta sia .jpg che .JPG)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(root, file)
                
                # Crea la cartella di destinazione
                rel_path = os.path.relpath(root, input_folder)
                target_dir = os.path.join(output_folder, rel_path)
                os.makedirs(target_dir, exist_ok=True)

                out_path = os.path.join(target_dir, file)

                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        w_width = int(base.width * 0.15)
                        w_height = int(wm.height * (w_width / watermark.width))
                        wm_resized = wm.resize((w_width, w_height))

                        # Incolla
                        base.paste(wm_resized, (base.width - w_width - 20, base.height - w_height - 20), wm_resized)
                        base.convert("RGB").save(out_path, "JPEG", quality=90)
                        print(f"Elaborato: {file}")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"Lavoro finito! Immagini elaborate: {count}")

if __name__ == "__main__":
    aggiungi_watermark()
