import os
from PIL import Image

def comprimi_solo_01():
    base_path = os.getcwd()
    
    # Estensioni supportate
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    count = 0
    print(f"Inizio scansione in: {base_path}")

    for root, dirs, files in os.walk(base_path):
        # Evita le cartelle di sistema di GitHub
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            nome_file, ext = os.path.splitext(file)
            
            # FILTRO CRITICO: Solo file che si chiamano esattamente '01'
            if nome_file == '01' and ext.lower() in valid_extensions:
                file_path = os.path.join(root, file)
                
                try:
                    with Image.open(file_path) as img:
                        # Se è un PNG con trasparenza, lo convertiamo in RGB per comprimerlo meglio
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        # Comprimiamo con qualità 70 (ottimo bilanciamento peso/qualità)
                        img.save(file_path, "JPEG", quality=70, optimize=True)
                        
                    print(f"COMPRESSO: {file_path}")
                    count += 1
                except Exception as e:
                    print(f"Errore su {file}: {e}")

    print(f"--- FINE --- Totale immagini '01' compresse: {count}")

if __name__ == "__main__":
    comprimi_solo_01()
