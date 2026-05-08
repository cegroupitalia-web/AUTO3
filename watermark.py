import os
from PIL import Image, ImageDraw, ImageFont

def applica_watermark_monstre():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print("--- MODALITÀ SCRITTE MONSTRE (150% WIDTH) ---")

    count = 0
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path).convert("RGBA") as base:
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        
                        # DIMENSIONE ESAGERATA: 150% della larghezza immagine
                        font_size = int(base.width * 1.5) 
                        
                        # Opacità decisa per coprire bene tutto
                        colore_testo = (0, 0, 0, 130) 
                        
                        try:
                            # Carichiamo il font
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        # Ne disegniamo poche, perché una sola occupa tutto lo spazio
                        # Posizionate al centro e sfalsate
                        for y in range(0, base.height, font_size // 2):
                            d.text((-font_size // 4, y), testo_pattern, fill=colore_testo, font=font)
                        
                        # Uniamo i livelli
                        base = Image.alpha_composite(base, txt_layer)

                        # LOGO SINGOLO (sempre 10% come richiesto prima)
                        if os.path.exists(watermark_path):
                            with Image.open(watermark_path).convert("RGBA") as wm_logo:
                                w_width = int(base.width * 0.10)
                                w_height = int(wm_logo.height * (w_width / wm_logo.width))
                                wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                                base.paste(wm_resized, (base.width - w_width - 20, base.height - w_height - 20), wm_resized)

                        # Salvataggio
                        base.convert("RGB").save(img_path, "JPEG", quality=95)
                        print(f"Applicato a: {file}")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"Finito! Elaborate {count} foto con scritte giganti.")

if __name__ == "__main__":
    applica_watermark_monstre()
