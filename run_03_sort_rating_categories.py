from csv_extras import csv_read, csv_write


def main():
    print("Sort rating categories")
    rs = csv_read("./data/rating.csv")
    cs = csv_read("./data/categories.csv")

    cs = {row["Name"]: row for row in cs}
    data = [
        {**it, **cs[it["Name"]]}
        for it in rs
    ]
    data = sorted(data, key=lambda x: (x["MainCategory"], -float(x["Rating"])))
    rs = [{"Name": it["Name"], "Rating": it["Rating"]}
          for it in data]
    cs = [{"Name": it["Name"], "MainCategory": it["MainCategory"], "Categories": it["Categories"]}
          for it in data]

    csv_write("./data/rating.csv", rs)
    csv_write("./data/categories.csv", cs)


if __name__ == "__main__":
    main()
