from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal
from csv_extras import csv_read
from string import Template


ENCODING = "utf-8"


@dataclass
class Field:
    key: str
    title: str
    align: Literal["left", "right", "center"]


Write = Callable[[str], None]


def generate_table(write: Write, fields: list[Field], rows: list[dict[str, str]]):
    lenghts = {}
    for it in fields:
        lenghts[it.key] = max(3, len(it.title))
    for row in rows:
        for it in fields:
            lenghts[it.key] = max(lenghts[it.key], len(row[it.key]))

    def write_row(row: dict[str, str]):
        write("| ")
        for i, it in enumerate(fields):
            if i > 0:
                write(" ")
            if it.align == 'left':
                write(row[it.key].ljust(lenghts[it.key]))
            elif it.align == 'right':
                write(row[it.key].rjust(lenghts[it.key]))
            else:
                write(row[it.key].center(lenghts[it.key]))
            write(" |")

    def align(field: Field):
        n = lenghts[field.key]
        if field.align == 'center':
            return ":" + "-" * (n - 2) + ":"
        if field.align == 'left':
            return ":" + "-" * (n - 1) + ""
        if field.align == 'right':
            return "" + "-" * (n - 2) + ":"
        return "-" * (n - 0)

    write_row({it.key: it.title for it in fields})
    write("\n")
    write_row({it.key: align(it) for it in fields})
    for row in rows:
        write("\n")
        write_row(row)


class WriteText:
    def __init__(self) -> None:
        self.parts = []

    def write(self, text):
        self.parts.append(text)

    def to_string(self):
        return "".join(self.parts)


def generate_rating(rows):
    fields = [
        Field("Ix", "", "left"),
        Field("Rating", "Rating", "center"),
        Field("Name", "Name", "left"),
        Field("Categories", "Categories", "right")
    ]
    w = WriteText()
    generate_table(w.write, fields, [
        dict(Ix=str(i+1), **row)
        for i, row in enumerate(rows)
    ])
    return w.to_string()


def generate_top_categories(data):
    top_categories = [
        dict(Ix=str(i+1), cat=cat, count=str(count))
        for i, (cat, count) in enumerate(Counter([
            cat
            for item in data
            for cat in item["Categories"].split(", ")
        ]).most_common(3))
    ]
    fields = [
        Field("Ix", "", "left"),
        Field("cat", "Categoria", "left"),
        Field("count", "Qtd.", "center"),
    ]
    w = WriteText()
    generate_table(w.write, fields, top_categories)
    return w.to_string()


def load_cs_map():
    cs_en = Path(
        "./data/categories.txt").read_text(encoding=ENCODING).splitlines()
    cs_pt = Path(
        "./data/categories_pt.txt").read_text(encoding=ENCODING).splitlines()
    return dict(zip(cs_en, cs_pt))


def format_categories(categories: str, cs_map: dict):
    return ", ".join(cs_map[it] for it in categories.split(","))


def main():
    print("Generate markdown")
    top_dramas = {
        "Milagre na Cela 7",
        "A Caminho do Céu",
        "Tudo Bem Não Ser Normal",
        "O Som da Magia",
    }
    top_comedy = {
        "Loucos Um Pelo Outro",
        "O Tio de Outro Mundo",
        "Sr. Rainha",
        "Um Homem Sem Filtros",
    }
    top_others = {
        "Messiah",
        "JUNG_E",
        "O Problema dos 3 Corpos",
        "Gato de Botas 2",
        "Crônicas de Arthdal",
    }
    top_gore = {
        "The 8 Show",
        "Psycho-Pass",
        "Parasyte",
        "A Lição",
        "Juvenile Justice",
    }

    rs = csv_read("./data/rating.csv")
    cs = csv_read("./data/categories.csv")
    cs_map = load_cs_map()
    data = [{**r, **c} for r, c in zip(rs, cs)]
    for row in data:
        if row["Name"] in top_dramas:
            row["Name"] = row["Name"] + " **(1)**"
        if row["Name"] in top_comedy:
            row["Name"] = row["Name"] + " **(2)**"
        if row["Name"] in top_others:
            row["Name"] = row["Name"] + " **(3)**"
        if row["Name"] in top_gore:
            row["Name"] = row["Name"] + " **(!)**"
        row["Categories"] = format_categories(row["Categories"], cs_map)

    movies = [row for row in data if row["MainCategory"] == "Movie"]
    series = [row for row in data if row["MainCategory"] == "Series"]
    animes = [row for row in data if row["MainCategory"] == "Anime"]
    miniseries = [row for row in data if row["MainCategory"] == "Miniseries"]

    template = Template(Path("./templates/rating_review.md")
                        .read_text(encoding=ENCODING)
                        # Hack to keeps markdown highlight
                        .replace("\\$", "$"))
    result = template.substitute(
        top_categories=generate_top_categories(data),
        top_top_categories=generate_top_categories([row for row in data
                                                    if float(row["Rating"]) > 9.49]),
        movies_table=generate_rating(movies),
        series_table=generate_rating(series),
        animes_table=generate_rating(animes),
        miniseries_table=generate_rating(miniseries),
    )
    Path("./output/rating_review.md").write_text(result,
                                                 encoding=ENCODING, newline="\n")


if __name__ == "__main__":
    main()
