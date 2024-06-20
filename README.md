# Scraping Inspire Posts by URL Pagination

## About Inspire
Inspire is the world’s largest online health community, patient engagement and real-world data platform. More than 10 million people each year come to Inspire to learn about their conditions and find peer support. Inspire also works with leading biopharmaceutical companies to provide insights about the patient experience, connect patients with life-advancing clinical trials and enable medical breakthroughs.

Inspire hosts a dedicated community of nearly 140,000 EDS patients, in partnership with the Ehlers-Danlos Society. You can learn more about Inspire and its health communities at www.Inspire.com.

## Overview
The URL Posts Downloader is a Python script designed to scrape posts from inspire.com website. The script uses the `requests` library to fetch pages and `BeautifulSoup` for parsing HTML content.

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

## Demonstration
![Script in action](/static/render1718926585112.gif)

## Disclaimer
Before using this scraper, please refer to the [Terms of Use](https://www.inspire.com/about/terms/) of the Inspire website. Ensure that you have the appropriate permissions to scrape data from the website. The developers of this script will not be liable for any consequences that may arise from its use, including any violations of the Terms of Use.
