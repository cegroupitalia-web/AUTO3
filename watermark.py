import os
from PIL import Image

def aggiungi_watermark():
    base_path = os.getcwd()
    # Entrata e Uscita puntano entrambe a AUTO3
    input_folder = os.path.join(base_path, 'AUTO3')
    watermark_path = os.path.join(base_path, 'watermark.png')

    print(f"--- INIZIO SOVRASCRITTURA ---")
    
    if not os.path.exists(input_folder):
        print(f"ERRORE: Cartella 'AUTO3' non trovata!")
        return

    if not os.path.exists(watermark_path):
        print(f"ERRORE: File 'watermark.png' non trovato!")
        return

    wm = Image.open(watermark_path).convert("RGBA")
    count = 0

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # Dimensioni watermark (20% della larghezza foto)
                        w_width = int(base.width * 0.20)
                        w_height = int(wm.height * (w_width / wm.width))
                        wm_resized = wm.resize((w_width, w_height), Image.Resampling.LANCZOS)

                        # Posizione (Basso a destra)
                        pos = (base.width - w_width - 20, base.height - w_height - 20)
                        base.paste(wm_resized, pos, wm_resized)
                        
                        # SOVRASCRIVE IL FILE ORIGINALE
                        base.convert("RGB").save(img_path, "JPEG", quality=90)
                        print(f"Sovrascritta: {file}")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE ---")
    print(f"Totale immagini modificate: {count}")

if __name__ == "__main__":
    aggiungi_watermark()
