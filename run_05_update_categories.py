from csv_extras import csv_read, csv_write


def main():
    print("Update categories")
    cs = csv_read("./data/categories.csv")
    ms = csv_read("./tmp/titles_miniseries.csv")

    ms = {it["Name"] for it in ms}

    for c in cs:
        if c["Name"] in ms:
            c["MainCategory"] = "Miniseries"

    csv_write("./data/categories.csv", cs)


if __name__ == "__main__":
    main()
