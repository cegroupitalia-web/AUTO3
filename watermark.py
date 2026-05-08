import os
from PIL import Image, ImageDraw, ImageFont

def applica_watermark_maxi():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print("--- AVVIO: SCRITTE 5X PIÙ GRANDI + LOGO 10% ---")

    if not os.path.exists(watermark_path):
        print("AVVISO: watermark.png non trovato, procedo solo con testo.")

    count = 0
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path) as img:
                        # Pulizia base
                        base = img.convert("RGBA")
                        
                        # --- 1. PATTERN TESTO GIGANTE (35% della larghezza) ---
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        
                        # Font 5 volte più grande (era 0.07, ora 0.35)
                        font_size = int(base.width * 0.35) 
                        colore_testo = (0, 0, 0, 70) # Opacità media
                        
                        try:
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        # Distribuzione larga per scritte giganti
                        for x in range(-font_size, base.width, font_size):
                            for y in range(-font_size, base.height, font_size):
                                d.text((x, y), testo_pattern, fill=colore_testo, font=font)
                        
                        base = Image.alpha_composite(base, txt_layer)

                        # --- 2. LOGO SINGOLO (10%) ---
                        if os.path.exists(watermark_path):
                            with Image.open(watermark_path).convert("RGBA") as wm_logo:
                                w_width = int(base.width * 0.10)
                                w_height = int(wm_logo.height * (w_width / wm_logo.width))
                                wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                                pos = (base.width - w_width - 30, base.height - w_height - 30)
                                base.paste(wm_resized, pos, wm_resized)

                        # --- 3. SALVATAGGIO ---
                        base.convert("RGB").save(img_path, "JPEG", quality=90)
                        print(f"OK: {file}")
                        count += 1
                        
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- Elaborati {count} file.")

if __name__ == "__main__":
    applica_watermark_maxi()
