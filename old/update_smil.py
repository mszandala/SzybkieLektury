#!/usr/bin/env python3
import re
from pathlib import Path
import sys

def main():
    smil_path = Path("audio.smil")

    if not smil_path.exists():
        print(f"Plik '{smil_path}' nie istnieje. Umieść skrypt w tym samym folderze co audio.smil.")
        sys.exit(1)

    print("MAPOWANIE: rozdział 1 -> part2.xhtml, rozdział 2 -> part3.xhtml, ...")
    chap = input("Podaj numer rozdziału do poprawy (np. 2): ").strip()
    if not chap.isdigit():
        print("Błąd: podaj numer (liczbę).")
        return
    chapter = int(chap)
    if chapter < 1:
        print("Błąd: numer rozdziału musi być >= 1.")
        return

    part_filename = f"part{chapter+1}.xhtml"   # rozdział 1 => part2.xhtml
    prev_part_filename = f"part{chapter}.xhtml"

    # wczytaj cały plik
    text = smil_path.read_text(encoding="utf-8")

    # znajdź największy sec w poprzednim rozdziale
    prev_pattern = re.compile(re.escape(prev_part_filename) + r'#sec(\d+)')
    prev_nums = [int(m.group(1)) for m in prev_pattern.finditer(text)]
    last_prev = max(prev_nums) if prev_nums else 0
    if chapter > 1 and last_prev == 0:
        print(f"⚠️  Nie znaleziono żadnych odwołań do '{prev_part_filename}'. Numeracja zostanie rozpoczęta od 1.")

    start = last_prev + 1

    # wzorzec do zamiany
    curr_pattern = re.compile(r'(' + re.escape(part_filename) + r'#sec)(\d+)')
    current = start

    def repl(m):
        nonlocal current
        out = f"{m.group(1)}{current}"
        current += 1
        return out

    new_text, count = curr_pattern.subn(repl, text)

    if count == 0:
        print(f"❌ Nie znaleziono odwołań do '{part_filename}' — nic nie zmieniono.")
        return

    # nadpisz plik oryginalny
    smil_path.write_text(new_text, encoding="utf-8")

    print(f"✅ Zmieniono {count} wpisów dla '{part_filename}'.")
    print(f"Plik '{smil_path}' został zaktualizowany.")

if __name__ == "__main__":
    main()
