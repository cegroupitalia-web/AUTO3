import os
from PIL import Image

def compressione_estrema():
    target_dir = os.path.join(os.getcwd(), "AUTO3")
    
    if not os.path.exists(target_dir):
        print(f"Errore: La cartella {target_dir} non esiste!")
        return

    count = 0
    # Larghezza massima desiderata (es. 1200 pixel) per risparmiare peso
    MAX_WIDTH = 1200 

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            nome, est = os.path.splitext(file)
            
            if nome == "01" and est.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                path_completo = os.path.join(root, file)
                
                try:
                    with Image.open(path_completo) as img:
                        # 1. Convertiamo in RGB (toglie la trasparenza pesante dei PNG)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        # 2. Ridimensionamento proporzionale (se l'immagine è più grande di MAX_WIDTH)
                        if img.width > MAX_WIDTH:
                            w_percent = (MAX_WIDTH / float(img.width))
                            h_size = int((float(img.height) * float(w_percent)))
                            img = img.resize((MAX_WIDTH, h_size), Image.Resampling.LANCZOS)
                        
                        # 3. Salvataggio con Qualità molto bassa (30) e ottimizzazione
                        # progressive=True rende il caricamento web più fluido
                        img.save(path_completo, "JPEG", quality=30, optimize=True, progressive=True)
                        
                        print(f"ESTREMA: {path_completo} (Ridotta a {MAX_WIDTH}px)")
                        count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"\n--- COMPRESSIONE MASSIMA ULTIMATA ---")
    print(f"Immagini '01' polverizzate: {count}")

if __name__ == "__main__":
    compressione_estrema()
