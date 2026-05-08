import os
from PIL import Image, ImageDraw, ImageFont

def applica_tutto():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print("--- INIZIO ELABORAZIONE (LOGO 5% + PATTERN TESTO) ---")

    # Carichiamo il logo
    wm_logo = None
    if os.path.exists(watermark_path):
        wm_logo = Image.open(watermark_path).convert("RGBA")
    else:
        print("AVVISO: watermark.png non trovato!")

    count = 0
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # --- 1. PATTERN TESTO (MOLTO LEGGERO) ---
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        
                        font_size = int(base.width * 0.03) 
                        colore_testo = (0, 0, 0, 25) # Opacità leggermente ridotta (più elegante)
                        
                        try:
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        for x in range(0, base.width, font_size * 6):
                            for y in range(0, base.height, font_size * 4):
                                shift = (y // (font_size * 4)) % 2 * (font_size * 3)
                                d.text((x + shift, y), testo_pattern, fill=colore_testo, font=font)
                        
                        base = Image.alpha_composite(base, txt_layer)

                        # --- 2. LOGO RIDOTTO AL 5% (DIMEZZATO) ---
                        if wm_logo:
                            # 0.05 significa il 5% della larghezza della foto
                            w_width = int(base.width * 0.05)
                            w_height = int(wm_logo.height * (w_width / wm_logo.width))
                            wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                            
                            # Posizione in basso a destra con margine di 20px
                            pos = (base.width - w_width - 20, base.height - w_height - 20)
                            base.paste(wm_resized, pos, wm_resized)

                        # --- 3. SALVATAGGIO ---
                        base.convert("RGB").save(img_path, "JPEG", quality=85)
                        print(f"OK: {file}")
                        count += 1
                        
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- Elaborati {count} file.")

if __name__ == "__main__":
    applica_tutto()
