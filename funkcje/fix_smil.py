import xml.etree.ElementTree as ET
from pathlib import Path
import re

NS = {"smil": "http://www.w3.org/ns/SMIL"}

def replace_text_dynamic_clean(smil_file: Path, output_file: Path):
    ET.register_namespace("", "http://www.w3.org/ns/SMIL")
    tree = ET.parse(str(smil_file))
    root = tree.getroot()

    for par in root.findall(".//smil:par", NS):
        audio = par.find("smil:audio", NS)
        text = par.find("smil:text", NS)
        if audio is not None and text is not None:
            audio_src = audio.attrib.get("src", "")
            match = re.match(r"book(\d+)\.mp3", audio_src)
            if match:
                N = int(match.group(1))
                old_src = text.attrib.get("src", "")
                if old_src.startswith("part2.xhtml"):
                    sec_part = old_src.split("#")[1] if "#" in old_src else ""
                    new_part_num = N + 2
                    new_src = f"part{new_part_num}.xhtml#{sec_part}".strip()
                    text.set("src", new_src)

    # zapisujemy do stringa i usuwamy spacje przed />
    xml_str = ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")
    xml_str = xml_str.replace(" />", "/>")

    # dodajemy deklarację XML
    xml_str = '<?xml version="1.0" encoding="utf-8"?>' + xml_str

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"Zapisano naprawiony plik: {output_file}")

def run():
    """Automatycznie szuka plików .smil w folderze temp i naprawia je"""
    temp_folder = Path("temp")
    
    if not temp_folder.exists():
        print("Błąd: Folder 'temp' nie istnieje!")
        return
    
    # Szukamy plików .smil w folderze temp
    smil_files = list(temp_folder.glob("*.smil"))
    
    if not smil_files:
        print("Błąd: Nie znaleziono plików .smil w folderze temp!")
        return
    
    print(f"Znaleziono {len(smil_files)} plików .smil")
    
    # Naprawiamy każdy plik .smil
    for smil_file in smil_files:
        print(f"\nNaprawiam plik: {smil_file.name}")
        output_file = temp_folder / f"fixed_{smil_file.name}"
        replace_text_dynamic_clean(smil_file, output_file)
    
    print(f"\nZakończono naprawianie {len(smil_files)} plików .smil")
