# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
# ]
# ///
import run_01_split_titles
import run_02_check_dups
import run_03_sort_rating_categories
import run_04_check_categories
import run_05_update_categories
import run_06_generate_markdown

run_01_split_titles.main()
run_02_check_dups.main()
run_03_sort_rating_categories.main()
run_04_check_categories.main(show=False)
run_05_update_categories.main()
run_06_generate_markdown.main()
