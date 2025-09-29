import sys
from bs4 import BeautifulSoup
import re
import os

def get_last_sec_number(file):
    """Zwraca największy numer sec w pliku"""
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")
    ids = [tag["id"] for tag in soup.find_all(attrs={"id": True}) if tag["id"].startswith("sec")]
    numbers = [int(re.match(r"sec(\d+)", i).group(1)) for i in ids if re.match(r"sec(\d+)", i)]
    return max(numbers) if numbers else 0

def renumber_file(file, start_counter):
    """Renumeruje tylko istniejące ID sec w pliku i zwraca następny numer"""
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")

    tags = [tag for tag in soup.find_all(attrs={"id": True}) if tag["id"].startswith("sec")]

    counter = start_counter
    for tag in tags:
        tag["id"] = f"sec{counter}"
        counter += 1

    out_file = os.path.splitext(file)[0] + "_fixed.xhtml"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"✅ Zapisano {out_file}, nadpisanych sec: {len(tags)}")
    return counter  # następny numer

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Użycie: python auto_fix_ids_xhtml_multi.py ref_file.xhtml file_to_fix1.xhtml [file_to_fix2.xhtml ...]")
        sys.exit(1)

    ref_file = sys.argv[1]           # pierwszy plik tylko jako referencja
    files_to_fix = sys.argv[2:]      # reszta plików do nadpisania

    # licznik zaczyna się od ostatniego sec w referencyjnym pliku + 1
    counter = get_last_sec_number(ref_file) + 1

    for file in files_to_fix:
        counter = renumber_file(file, counter)
