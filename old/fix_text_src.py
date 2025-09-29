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

    print(f"Zapisano plik: {output_file}")

# Przykład użycia:
replace_text_dynamic_clean(Path("audio.smil"), Path("audio.fixed.smil"))
