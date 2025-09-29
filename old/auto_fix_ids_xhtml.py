import sys
from bs4 import BeautifulSoup
import re

def get_last_sec_number(prev_file):
    with open(prev_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")
    ids = [tag["id"] for tag in soup.find_all(attrs={"id": True}) if tag["id"].startswith("sec")]

    numbers = []
    for i in ids:
        m = re.match(r"sec(\d+)", i)  # wyciąga tylko czystą liczbę po 'sec'
        if m:
            numbers.append(int(m.group(1)))

    if not numbers:
        return 0
    return max(numbers)


def process_file(prev_file, curr_file):
    # znajdź ostatni sec w poprzednim pliku
    last_sec = get_last_sec_number(prev_file)
    counter = last_sec + 1

    # wczytaj bieżący plik
    with open(curr_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")

    # wszystkie <h1>, <h2>, <p> i <div class="block">
    tags = []
    for tag in soup.find_all(True):

        # 1. Cały div.block traktujemy jako jeden sec
        if tag.name == "div" and "block" in tag.get("class", []):
            tags.append(tag)
            continue

        # 2. Pomijamy WSZYSTKIE elementy wewnątrz div.block
        if tag.find_parent(lambda t: t.name == "div" and "block" in t.get("class", [])):
            continue

        # 3. Nagłówki i paragrafy poza blokami
        if tag.name in ["h1", "h2", "p"]:
            tags.append(tag)


    new_added = 0  # licznik ile nowych sec dodano

    for tag in tags:
        # pomiń jeśli już ma id zaczynające się od sec
        if tag.has_attr("id") and tag["id"].startswith("sec"):
            continue

        preview = tag.get_text(strip=True)[:80]  # pokaz początek tekstu
        proposed_id = f"sec{counter}"

        user_input = input(f"\nTekst: {preview}\nProponowane id: {proposed_id} → ")

        if user_input.strip() == "":
            tag["id"] = proposed_id  # akceptuj
            new_added += 1
            counter += 1
        elif user_input.strip().lower() == "s":
            print("⏭ Pominięto")
            continue
        else:
            tag["id"] = user_input.strip()  # ręcznie ustawione ID
            if tag["id"].startswith("sec"):
                new_added += 1
                try:
                    counter = int(tag["id"].replace("sec", "")) + 1
                except ValueError:
                    counter += 1
            else:
                counter += 1

    # zapisz nowy plik
    out_file = curr_file.replace(".xhtml", ".xhtml")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"\n✅ Zapisano poprawiony plik: {out_file}")
    print(f"Dodano nowych sec: {new_added}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie: python fix_ids.py part2.xhtml part3.xhtml")
        sys.exit(1)

    prev_file = sys.argv[1]
    curr_file = sys.argv[2]

    process_file(prev_file, curr_file)




