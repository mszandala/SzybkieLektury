from bs4 import BeautifulSoup

def process_file_single(curr_file):
    counter = 1

    with open(curr_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")

    tags = []
    for tag in soup.find_all(True):
        # Pomijamy wszystkie elementy wewnątrz div.block
        if tag.find_parent(lambda t: t.name == "div" and "block" in t.get("class", [])):
            continue

        # Cały div.block traktujemy jako jeden sec
        if tag.name == "div" and "block" in tag.get("class", []):
            tags.append(tag)
            continue

        # Nagłówki i paragrafy poza blokami
        if tag.name in ["h1", "h2", "p"]:
            tags.append(tag)

    new_added = 0

    for tag in tags:
        # Pomijamy jeśli:
        # - już ma id zaczynające się od sec
        # - lub ma klasę spacer
        # - lub jest pusty / tylko białe znaki
        if tag.has_attr("id") and tag["id"].startswith("sec"):
            continue
        if "spacer" in tag.get("class", []):
            continue
        if not tag.get_text(strip=True):
            continue

        tag["id"] = f"sec{counter}"
        counter += 1
        new_added += 1

    out_file = curr_file.replace(".xhtml", ".fixed.xhtml")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"✅ Zapisano poprawiony plik: {out_file}")
    print(f"Dodano nowych sec: {new_added}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Użycie: python fix_ids_single.py plik.xhtml")
        sys.exit(1)

    curr_file = sys.argv[1]
    process_file_single(curr_file)
