import os
from PIL import Image, ImageDraw, ImageFont

def applica_watermark_definitivo():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print(f"Lavoro in corso nella cartella: {base_path}")
    
    count = 0
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        # --- PATTERN TESTO (GRANDE E VISIBILE) ---
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        font_size = int(base.width * 0.07) # 7% della larghezza
                        colore_testo = (0, 0, 0, 100) # Nero molto più visibile
                        
                        try:
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        # Griglia di scritte
                        for x in range(0, base.width, font_size * 5):
                            for y in range(0, base.height, font_size * 3):
                                d.text((x, y), testo_pattern, fill=colore_testo, font=font)
                        
                        base = Image.alpha_composite(base, txt_layer)

                        # --- LOGO SINGOLO (10%) ---
                        if os.path.exists(watermark_path):
                            with Image.open(watermark_path).convert("RGBA") as wm_logo:
                                w_width = int(base.width * 0.10)
                                w_height = int(wm_logo.height * (w_width / wm_logo.width))
                                wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                                pos = (base.width - w_width - 30, base.height - w_height - 30)
                                base.paste(wm_resized, pos, wm_resized)

                        # SALVATAGGIO: Usiamo qualità 94 per cambiare il peso del file
                        base.convert("RGB").save(img_path, "JPEG", quality=94, optimize=True)
                        print(f"FILE MODIFICATO CON SUCCESSO: {file}")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- Totale foto aggiornate: {count}")

if __name__ == "__main__":
    applica_watermark_definitivo()
