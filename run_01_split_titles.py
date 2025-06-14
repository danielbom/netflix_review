# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
# ]
# ///
import pandas as pd
from pathlib import Path


def main():
    print("Split titles")
    try:
        df0 = pd.read_csv("./data/NetflixRawData.csv")
    except FileNotFoundError:
        print("Warning: './data/NetflixRawData.csv' not found, using ./data/NetflixRawDataSample.csv")
        df0 = pd.read_csv("./data/NetflixRawDataSample.csv")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        exit(1)

    Path("./tmp").mkdir(exist_ok=True)

    # initial columns: Title,Date
    df0["Date"] = df0["Date"]
    df0["Title"] = df0["Title"]
    df1 = df0.sort_values("Title").reset_index(drop=True)

    dfs2 = df1[df1["Title"].str.contains(
        r": Temporada \d+", regex=True, na=False)].copy()
    dfs2["Name"] = dfs2["Title"].str.replace(
        r": Temporada \d+.*$", "", regex=True)
    dfs2["Season"] = dfs2["Title"].str.extract(
        r": Temporada (\d+)", expand=False).astype(int)
    dfg = dfs2.groupby(["Name", "Season"]).agg(
        Episodes=("Title", "count")).reset_index()
    dfg = dfg.groupby("Name", as_index=False).agg(
        {"Season": "max", "Episodes": "sum"})
    dfg = dfg[dfg.groupby("Name")["Season"].transform("max") == dfg["Season"]]
    dfg_single = dfg[(dfg["Episodes"] == 1) & (dfg["Season"] == 1)]
    dfg_multi = dfg[~((dfg["Episodes"] == 1) & (dfg["Season"] == 1))]
    dfg_single.to_csv("./tmp/titles_series_unwatched.csv", index=False)
    dfg_multi.to_csv("./tmp/titles_series.csv", index=False)
    df2: pd.DataFrame = df1[~df1.index.isin(dfs2.index)].copy()

    dfms = df2[df2["Title"].str.contains(": Minissérie:", na=False)].copy()
    dfms["Name"] = dfms["Title"].str.replace(
        r": Minissérie:.*", "", regex=True)
    dfg = dfms.groupby("Name").agg(Episodes=("Title", "count")).reset_index()
    dfg_multi = dfg[~((dfg["Episodes"] == 1))]
    dfg_multi.to_csv("./tmp/titles_miniseries.csv", index=False)
    dfg_single = dfg[(dfg["Episodes"] == 1)]
    dfg_single.to_csv("./tmp/titles_miniseries_unwatched.csv", index=False)
    df3: pd.DataFrame = df2[~df2.index.isin(dfms.index)]

    dfs1 = df3[df3["Title"].str.contains(
        r"Episódio \d+$", regex=True, na=False)].copy()
    dfs1["Name"] = dfs1["Title"].str.replace(r": Episódio \d+", "", regex=True)
    dfs1["Episode"] = dfs1["Title"].str.extract(
        r": Episódio (\d+)", expand=False).astype(int)
    dfg = dfs1.groupby("Name").agg(Episodes=("Episode", "count")).reset_index()
    dfg_multi = dfg[~((dfg["Episodes"] == 1))]
    dfg_multi.to_csv("./tmp/titles_series_single.csv", index=False)
    dfg_single = dfg[(dfg["Episodes"] == 1)]
    dfg_single.to_csv("./tmp/titles_series_single_unwatched.csv", index=False)
    df4: pd.DataFrame = df3[~df3.index.isin(dfs1.index)].copy()

    df4["Name"] = df4["Title"].str.extract(r"^([^:]+):?", expand=False)
    dfg = df4.groupby("Name").agg(Episodes=("Title", "count")).reset_index()

    dfm = dfg[dfg["Episodes"] == 1][["Name"]]
    dfm.to_csv("./tmp/titles_maybe_movies.csv", index=False)
    dfs = dfg[dfg["Episodes"] > 1]
    dfs.to_csv("./tmp/titles_maybe_series.csv", index=False)


if __name__ == "__main__":
    main()
