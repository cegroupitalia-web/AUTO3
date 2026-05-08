import os
from PIL import Image

def aggiungi_watermark():
    # 1. Setup percorsi
    base_path = os.getcwd()
    input_folder = os.path.join(base_path, 'AUTO3')
    output_folder = os.path.join(base_path, 'AUTO3_PRONTE')
    watermark_path = os.path.join(base_path, 'watermark.png')

    print(f"--- INIZIO ELABORAZIONE ---")
    print(f"Cartella input cercata: {input_folder}")
    
    if not os.path.exists(input_folder):
        print(f"ERRORE: La cartella 'AUTO3' non esiste! Controlla se è scritta in MAIUSCOLO.")
        return

    if not os.path.exists(watermark_path):
        print(f"ERRORE: Il file 'watermark.png' non è nella cartella principale.")
        return

    wm = Image.open(watermark_path).convert("RGBA")
    count = 0

    # 2. Scansione ricorsiva (entra in tutte le sottocartelle)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Accetta TUTTO quello che sembra un'immagine (maiuscole o minuscole)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
                img_path = os.path.join(root, file)
                
                # Crea sottocartelle nell'output
                rel_path = os.path.relpath(root, input_folder)
                target_dir = os.path.join(output_folder, rel_path)
                os.makedirs(target_dir, exist_ok=True)

                out_path = os.path.join(target_dir, file)

                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # Dimensioni watermark (15% della larghezza)
                        w_width = int(base.width * 0.15)
                        w_height = int(wm.height * (w_width / wm.width))
                        wm_resized = wm.resize((w_width, w_height), Image.Resampling.LANCZOS)

                        # Posizione (Basso a destra)
                        pos = (base.width - w_width - 20, base.height - w_height - 20)
                        base.paste(wm_resized, pos, wm_resized)
                        
                        # Salva come RGB (compatibile con tutto)
                        base.convert("RGB").save(out_path, "JPEG", quality=85)
                        print(f"OK: Elaborata {file} in {rel_path}")
                        count += 1
                except Exception as e:
                    print(f"ERRORE su {file}: {e}")

    print(f"--- FINE ---")
    print(f"Totale immagini elaborate: {count}")

if __name__ == "__main__":
    aggiungi_watermark()
