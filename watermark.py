import os
from PIL import Image, ImageDraw, ImageFont

def applica_watermark_decisivo():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print(f"Cartella di lavoro attuale: {base_path}")
    
    if not os.path.exists(watermark_path):
        print("!!! ERRORE CRITICO: watermark.png NON TROVATO nella root !!!")
        # Non fermiamo tutto, proviamo almeno a fare le scritte
    else:
        print("Logo watermark.png trovato correttamente.")

    count = 0
    # Estensioni permesse
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    for root, dirs, files in os.walk(base_path):
        # Salta cartelle di sistema
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(valid_extensions) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # --- PATTERN TESTO GRANDE E VISIBILE ---
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        
                        # Font 6% della larghezza (bello grande)
                        font_size = int(base.width * 0.06) 
                        colore_testo = (0, 0, 0, 90) # Opacità decisa (90 su 255)
                        
                        try:
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        for x in range(0, base.width, font_size * 4):
                            for y in range(0, base.height, font_size * 3):
                                d.text((x, y), testo_pattern, fill=colore_testo, font=font)
                        
                        base = Image.alpha_composite(base, txt_layer)

                        # --- LOGO SINGOLO AL 10% ---
                        if os.path.exists(watermark_path):
                            with Image.open(watermark_path).convert("RGBA") as wm_logo:
                                w_width = int(base.width * 0.10)
                                w_height = int(wm_logo.height * (w_width / wm_logo.width))
                                wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                                pos = (base.width - w_width - 40, base.height - w_height - 40)
                                base.paste(wm_resized, pos, wm_resized)

                        # SALVATAGGIO FORZATO
                        base.convert("RGB").save(img_path, "JPEG", quality=95)
                        print(f"MODIFICATO: {file}")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- File totali modificati: {count}")

if __name__ == "__main__":
    applica_watermark_decisivo()
if __name__ == "__main__":
    applica_tutto()
