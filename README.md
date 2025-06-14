# Netflix Rating

This repository contains some scripts I created to analyze and give a rating score to the Netflix series I have watched until now. I always wanted to do such kind of analysis to remember some titles and facilitates my conversations about it.

I have used 'uv' as packaged manager, but my only dependecy is 'pandas'. So, feel free to check the steps and try it on your data.

I have downloaded the netflix data at "Manage Profiles" -> Select my profile (Profiles settings) -> "What was watched" -> "Download All".

The results can be found at:

- [Rating review](./output/rating_review.md)

## Get started

```bash
# Requires ./data/NetflixRawData.csv otherwise it will use a simple sample ./data/NetflixRawData.csv

# The steps 1-4 was used to group and split the data and help me during the rating classification process.

# Step by step
uv run ./run_01_split_titles.py
uv run ./run_02_check_dups.py
uv run ./run_03_sort_rating_categories.py
uv run ./run_04_check_categories.py
uv run ./run_05_update_categories.py
uv run ./run_06_generate_markdown.py

# Everything
uv run ./run.py
```
