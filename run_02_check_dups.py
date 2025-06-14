from pathlib import Path
import csv
from collections import Counter


def main():
    print("Check dups")
    def get_season(row):
        val = row.get("Season")
        return f" S{val}" if val else ""

    c = Counter()

    for path in Path("./tmp").absolute().glob("titles_*"):
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            names = [row['Name'] + get_season(row) for row in reader]
        c.update(names)

    dup = False
    for name, count in c.items():
        if count > 1:
            print(f"{name}: {count}")
            dup = True
    if dup:
        exit(1)


if __name__ == "__main__":
    main()
