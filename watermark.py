import os

def diagnosi():
    print("--- DIAGNOSI CARTELLE ---")
    base_path = os.getcwd()
    print(f"Directory attuale: {base_path}")
    
    # Elenca tutto quello che c'è nella cartella principale
    contenuto = os.listdir(base_path)
    print(f"File e cartelle trovati nella root: {contenuto}")
    
    # Prova a cercare AUTO3 in modo intelligente (senza badare a maiuscole/minuscole)
    trovata = False
    for voce in contenuto:
        if voce.lower() == 'auto3':
            print(f"AVVISO: Ho trovato una cartella che somiglia ad AUTO3, si chiama: '{voce}'")
            sotto_contenuto = os.listdir(os.path.join(base_path, voce))
            print(f"Contenuto di questa cartella: {sotto_contenuto[:5]}... (primi 5 file)")
            trovata = True
            
    if not trovata:
        print("ERRORE CRITICO: Non esiste nessuna cartella chiamata AUTO3 o simili!")

if __name__ == "__main__":
    diagnosi()
