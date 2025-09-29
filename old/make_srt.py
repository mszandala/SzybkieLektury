import xml.etree.ElementTree as ET
import sys
import os

def smil_to_srt(smil_file, xhtml_file, part_number, output_file):
    # Parsowanie pliku SMIL
    tree = ET.parse(smil_file)
    root = tree.getroot()

    # Parsowanie pliku XHTML
    xhtml_tree = ET.parse(xhtml_file)
    xhtml_root = xhtml_tree.getroot()
    ns_xhtml = {"xhtml": "http://www.w3.org/1999/xhtml"}

    # Mapa id -> tekst
    text_map = {}
    for elem in xhtml_root.findall(".//xhtml:*[@id]", ns_xhtml):
        elem_id = elem.attrib["id"]
        text_map[elem_id] = "".join(elem.itertext()).strip()

    # Funkcja konwersji czasu
    def format_time(t):
        seconds = float(t[:-1])
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    srt_lines = []
    counter = 1

    ns = {"smil": "http://www.w3.org/ns/SMIL"}
    for par in root.findall(".//smil:par", ns):
        text_elem = par.find("smil:text", ns)
        audio_elem = par.find("smil:audio", ns)

        if text_elem is not None and audio_elem is not None:
            src = text_elem.attrib["src"]
            if src.startswith(f"part{part_number}.xhtml"):
                sec_id = src.split("#")[1]
                if sec_id in text_map:
                    start = format_time(audio_elem.attrib["clipBegin"])
                    end = format_time(audio_elem.attrib["clipEnd"])
                    text_content = text_map[sec_id]

                    srt_lines.append(f"{counter}")
                    srt_lines.append(f"{start} --> {end}")
                    srt_lines.append(text_content)
                    srt_lines.append("")
                    counter += 1

    # Zapis
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    print(f"✔ Zapisano napisy do {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python make_srt.py [numer_części]")
        sys.exit(1)

    part_number = sys.argv[1]
    smil_file = "audio.smil"
    xhtml_file = f"part{part_number}.xhtml"
    output_file = f"part{part_number}.srt"

    if not os.path.exists(smil_file):
        print(f"❌ Nie znaleziono {smil_file}")
        sys.exit(1)
    if not os.path.exists(xhtml_file):
        print(f"❌ Nie znaleziono {xhtml_file}")
        sys.exit(1)

    smil_to_srt(smil_file, xhtml_file, part_number, output_file)
