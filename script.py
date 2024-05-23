import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import random
from tqdm import tqdm
import threading
from InquirerPy import inquirer, get_style
import argparse
import json
from termcolor import colored
from dataprocessor import remove_duplicate_posts

def load_communities_dict():
    try:
        with open('communities_dict.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(colored("Error: 'communities_dict.json' file not found.", "red"))
        exit(1)
    except json.JSONDecodeError:
        print(colored("Error: Failed to decode JSON from 'communities_dict.json'.", "red"))
        exit(1)

def get_random_user_agent(user_agent_list):
    return random.choice(user_agent_list)

def setup_session(user_agent_list):
    session = requests.Session()
    session.headers.update({'User-Agent': get_random_user_agent(user_agent_list)})
    return session

def configure_parser():
    parser = argparse.ArgumentParser(description="Scrape public community posts from Inspire.com's forums.")
    parser.add_argument("-np", "--numpages", help="Number of pages to scrape", type=int, default=40)
    parser.add_argument("-o", "--output", help="Output file path", type=str, default="posts_data.txt")
    return parser.parse_args()

def select_community(communities_dict):
    try:
        community_options = inquirer.fuzzy(
            message="Search and select a community from the list below:",
            choices=list(communities_dict.keys()),
            max_height="35%",
            border=True,
            style=get_style({
                "question": "green",
                "fuzzy_prompt": "orange",
                "fuzzy_info": "orange",
                "fuzzy_match": "orange",
                "questionmark": "cyan",
                "pointer": "#61afef",
            })
        ).execute()
        return communities_dict[community_options]
    except KeyError:
        print(colored("Error: Selected community not found in the dictionary.", "red"))
        exit(1)

def fetch_page(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(colored(f"Error fetching page: {e}", "red"))
        return None

def parse_posts(soup, base_url):
    try:
        posts = soup.select('.pb-head')
        post_urls = [urljoin(base_url, post.find('a', id='post-title-link').get('href')) for post in posts]
        return [url for url in post_urls if url.startswith(f"{base_url}discussion/")]
    except Exception as e:
        print(colored(f"Error parsing posts: {e}", "red"))
        return []

def process_post(session, post_url, output_file, file_lock):
    try:
        post_response = session.get(post_url)
        post_response.raise_for_status()
        post_soup = BeautifulSoup(post_response.content, "html.parser")
        post_title = post_soup.find('a', id='post-title-link').text.strip() if post_soup.find('a', id='post-title-link') else 'No title'
        post_content = post_soup.find("div", id="post-snippet").get_text(strip=True) if post_soup.find("div", id="post-snippet") else ""
        reply_divs = post_soup.find_all("div", id="replyContent")
        post_replies = " ".join([div.get_text(strip=True) for div in reply_divs])

        with file_lock:
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(f"Title: {post_title}\n")
                file.write(f"Content: {post_content}\n")
                file.write(f"Replies: {post_replies}\n")
                file.write("-------\n")
    except requests.RequestException as e:
        print(colored(f"Error fetching post: {e}", "red"))
    except Exception as e:
        print(colored(f"Error processing post: {e}", "red"))

def process_page(session, post_links, output_file):
    file_lock = threading.Lock()
    threads = [threading.Thread(target=process_post, args=(session, post_url, output_file, file_lock)) for post_url in post_links]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def get_last_post_stamp(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        stamp_text = soup.find('div', id='post-date').get_text(strip=True) if soup.find('div', id='post-date') else None
        stamp_str = "".join(stamp_text.split('•')) if stamp_text else None
        if "edited" in stamp_str:
            stamp_str = stamp_str.split("(edited")[0].strip()
        return datetime.strptime(stamp_str, "%b %d, %Y  %I:%M %p")
    except requests.RequestException as e:
        print(colored(f"Error fetching last post stamp: {e}", "red"))
        return None
    except Exception as e:
        print(colored(f"Error parsing last post stamp: {e}", "red"))
        return None

def main():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    ]
    session = setup_session(user_agent_list)
    communities_dict = load_communities_dict()
    args = configure_parser()
    community_name = select_community(communities_dict)
    base_url = f"https://www.inspire.com/groups/{community_name}/"
    url_params = "?p={}&section=topic&order=new&activeCursor=after"
    page_start_date = datetime.utcnow()

    try:
        with tqdm(total=args.numpages, desc="Scraping Pages!", unit="page") as pbar:
            for page in range(1, args.numpages + 1):
                url = base_url + url_params.format(page) + f"&after={page_start_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                response = fetch_page(session, url)
                if response is None:
                    continue
                soup = BeautifulSoup(response.content, "html.parser")
                post_links = parse_posts(soup, base_url)
                process_page(session, post_links, args.output)
                last_post_stamp = get_last_post_stamp(session, post_links[-1])
                if last_post_stamp is None:
                    continue
                page_start_date = last_post_stamp
                pbar.update(1)
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

    try:
        remove_duplicate_posts(args.output)
        print(colored("Done scraping!\n", "green"))
        print(colored("Your data has been saved to " + args.output + "\n", "light_cyan"))
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

if __name__ == "__main__":
    main()