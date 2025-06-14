import csv


def main(show=True):
    print("Check categories")
    with open("./data/categories.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        categories = {cat
                      for row in reader
                      for cat in row["Categories"].split(",")}

    with open("./data/categories.txt") as textfile:
        valid = {line.strip() for line in textfile}

    invalid = categories - valid
    if len(invalid) > 0:
        for cat in sorted(invalid):
            print("-", cat)
        raise Exception("Invalid categories found")
    elif show:
        print("List of categories:")
        for i, cat in enumerate(sorted(categories)):
            print(f"{i+1}.", cat)


if __name__ == "__main__":
    main()
