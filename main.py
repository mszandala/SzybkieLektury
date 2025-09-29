import funkcje.upload as upload
import funkcje.fix_smil as fix_smil

def menu():
    print("\n=== SzybkieLektury ===")
    """
    Etap 1: Wgranie plików
    """
    print("\nETAP 1: Wgranie plików")
    upload.run()

    """Etap 2: Naprawa plików SMIL
    """
    fix_smil.run()
    

if __name__ == "__main__":
    menu()