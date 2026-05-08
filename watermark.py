import os
from PIL import Image

def aggiungi_watermark():
    # Usiamo la cartella attuale come punto di partenza
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')

    print(f"--- INIZIO ELABORAZIONE ---")
    
    if not os.path.exists(watermark_path):
        print(f"ERRORE: File 'watermark.png' non trovato nella root!")
        return

    wm = Image.open(watermark_path).convert("RGBA")
    count = 0

    # Scansiona tutte le cartelle e sottocartelle partendo dalla root
    for root, dirs, files in os.walk(base_path):
        # Evitiamo di entrare nelle cartelle di sistema di GitHub
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            # Se il file è un'immagine e non è il watermark stesso
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # Dimensioni watermark (20% della larghezza della foto)
                        w_width = int(base.width * 0.20)
                        w_height = int(wm.height * (w_width / wm.width))
                        wm_resized = wm.resize((w_width, w_height), Image.Resampling.LANCZOS)

                        # Posizione: Basso a destra (con 20px di margine)
                        pos = (base.width - w_width - 20, base.height - w_height - 20)
                        base.paste(wm_resized, pos, wm_resized)
                        
                        # Salvataggio e sovrascrittura
                        base.convert("RGB").save(img_path, "JPEG", quality=90)
                        print(f"OK: {os.path.relpath(img_path, base_path)}")
                        count += 1
                except Exception as e:
                    print(f"ERRORE su {file}: {e}")

    print(f"--- FINE ---")
    print(f"Totale immagini modificate: {count}")

if __name__ == "__main__":
    aggiungi_watermark()
