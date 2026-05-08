import os
from PIL import Image, ImageDraw, ImageFont

def applica_watermark_ultra_giant():
    base_path = os.getcwd()
    watermark_path = os.path.join(base_path, 'watermark.png')
    testo_pattern = "cegroupitalia"

    print("--- MODALITÀ ULTRA GIGANTE ATTIVATA ---")

    count = 0
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and file != 'watermark.png':
                img_path = os.path.join(root, file)
                
                try:
                    with Image.open(img_path) as img:
                        # Reset per appiattire i vecchi loghi
                        base = img.convert("RGB").convert("RGBA")
                        
                        # --- 1. PATTERN TESTO "MONSTRO" ---
                        txt_layer = Image.new('RGBA', base.size, (0,0,0,0))
                        d = ImageDraw.Draw(txt_layer)
                        
                        # Grandezza esagerata: 80% della larghezza della foto per ogni scritta
                        font_size = int(base.width * 0.80) 
                        
                        # Opacità molto alta (160 su 255 è quasi nero pieno)
                        colore_testo = (0, 0, 0, 160) 
                        
                        try:
                            font = ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        # Griglia molto larga perché le scritte sono enormi
                        # Ne mettiamo poche ma giganti che coprono tutto
                        for x in range(-font_size // 2, base.width, font_size):
                            for y in range(-font_size // 2, base.height, font_size // 2):
                                d.text((x, y), testo_pattern, fill=colore_testo, font=font)
                        
                        base = Image.alpha_composite(base, txt_layer)

                        # --- 2. LOGO SINGOLO (10%) ---
                        if os.path.exists(watermark_path):
                            with Image.open(watermark_path).convert("RGBA") as wm_logo:
                                w_width = int(base.width * 0.10)
                                w_height = int(wm_logo.height * (w_width / wm_logo.width))
                                wm_resized = wm_logo.resize((w_width, w_height), Image.Resampling.LANCZOS)
                                pos = (base.width - w_width - 20, base.height - w_height - 20)
                                base.paste(wm_resized, pos, wm_resized)

                        # --- 3. SALVATAGGIO ---
                        base.convert("RGB").save(img_path, "JPEG", quality=95)
                        print(f"ULTRA-WATERMARK: {file}")
                        count += 1
                        
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- {count} immagini stravolte.")

if __name__ == "__main__":
    applica_watermark_ultra_giant()
