import csv


def csv_read(path: str):
    with open(path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def csv_write(path: str, data: list[dict]):
    with open(path, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
