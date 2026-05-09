import os
from PIL import Image

def compressione_reale_50():
    # Cerchiamo la cartella AUTO3 nella posizione corrente
    base_path = os.getcwd()
    target_dir = os.path.join(base_path, "AUTO3")
    
    if not os.path.exists(target_dir):
        print(f"ERRORE: Cartella {target_dir} non trovata!")
        # Provo a cercare in tutto il repository se AUTO3 non è nella root
        target_dir = base_path 

    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            nome, ext = os.path.splitext(file)
            
            # Filtro drastico: solo i file che si chiamano esattamente 01
            if nome == "01" and ext.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                path_completo = os.path.join(root, file)
                
                try:
                    with Image.open(path_completo) as img:
                        # 1. Forza la conversione in RGB (elimina pesi inutili)
                        img = img.convert("RGB")
                        
                        # 2. Calcolo dimensioni (Dimezzamento matematico)
                        w, h = img.size
                        nuovi_pixel = (int(w * 0.5), int(h * 0.5))
                        
                        # 3. Ridimensionamento con filtro pesante (LANCZOS)
                        img_ridotta = img.resize(nuovi_pixel, Image.Resampling.LANCZOS)
                        
                        # 4. Salvataggio con qualità BASSA (per vedere la differenza di peso)
                        img_ridotta.save(path_completo, "JPEG", quality=30, optimize=True)
                        
                        print(f"SUCCESSO: {file} ridotto a {nuovi_pixel[0]}x{nuovi_pixel[1]}")
                        count += 1
                except Exception as e:
                    print(f"ERRORE su {file}: {e}")

    print(f"--- FINE --- Ridotte {count} foto del 50%.")

if __name__ == "__main__":
    compressione_reale_50()
