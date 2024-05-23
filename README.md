# Scraping Inspire Posts by Manipulating URLs

## Overview
The URL Posts Scraper is a Python script designed to scrape posts from inspire.com website. The script uses the `requests` library to fetch pages and `BeautifulSoup` for parsing HTML content.

## Usage
To run the script, you can provide the number of pages to scrape and the output file path as command-line arguments.

```zsh
python script.py -np [number_of_pages] -o [output_file_path]
```
This script supports the following command-line arguments:
- `-np` or `--numpages`: Specify the number of pages to scrape. If no argument is provided, it will use the default value of 40 pages.
- `-o` or `--output`: Specify the output file path for the scraped data. If not provided, the default is `posts_data.txt`.

Upon running, you will also be prompted to select a community from a searchable dropdown list, ensuring that you scrape data from the specific community you are interested in.

Examples:
```zsh
python script.py -np 50 -o custom_output.txt    # Fetch 50 pages and output to custom_output.txt
python script.py                                # Fetch the default 40 pages and output to posts_data.txt
```

