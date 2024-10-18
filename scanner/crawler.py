import httpx
from bs4 import BeautifulSoup
from colorama import Fore
from urllib.parse import urljoin, urlparse

async def crawl_site(url, max_depth=2):
    """
    Crawls the given URL up to the specified depth, extracting forms and URLs.

    Args:
        url (str): The starting URL for the crawl.
        max_depth (int): The maximum depth to crawl.

    Returns:
        tuple: A list of discovered forms and a list of discovered URLs.
    """
    print(Fore.YELLOW + f"Crawling the website: {url}...")

    visited = set()
    to_visit = [(url, 0)]
    discovered_forms = []
    discovered_urls = set()

    async with httpx.AsyncClient() as client:
        while to_visit:
            current_url, depth = to_visit.pop(0)

            if current_url in visited or depth > max_depth:
                continue

            visited.add(current_url)

            try:
                response = await client.get(current_url)

                if response.status_code != 200:
                    print(Fore.RED + f"Failed to retrieve {current_url}, Status Code: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                forms = soup.find_all('form')
                discovered_forms.extend(forms)
                if forms:
                    print(Fore.GREEN + f"Found {len(forms)} forms on {current_url}.")

                links = extract_links(soup, current_url)
                for link in links:
                    if link not in visited:
                        discovered_urls.add(link)
                        to_visit.append((link, depth + 1))

                extract_scripts(soup, current_url, discovered_urls, to_visit, visited, depth)

                check_meta_refresh(soup, current_url, discovered_urls, to_visit, visited, depth)

                print(Fore.YELLOW + f"Crawled: {current_url}, Depth: {depth}, Queue: {len(to_visit)}")

            except Exception as e:
                print(Fore.RED + f"Error during crawling {current_url}: {e}")

    print(Fore.GREEN + f"Discovered {len(discovered_forms)} forms and {len(discovered_urls)} URLs.")
    return discovered_forms, list(discovered_urls)

def extract_links(soup, base_url):
    """
    Extracts and normalizes links from the given page.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
        base_url (str): The base URL for resolving relative links.

    Returns:
        list: A list of fully qualified URLs.
    """
    links = []
    for link_tag in soup.find_all('a', href=True):
        href = link_tag.get('href')
        full_url = urljoin(base_url, href)
        if urlparse(full_url).scheme in ['http', 'https']:
            links.append(full_url)
    return links

def extract_scripts(soup, base_url, discovered_urls, to_visit, visited, depth):
    """
    Extracts external script URLs and adds them to the crawl queue.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
        base_url (str): The base URL for resolving script URLs.
        discovered_urls (set): Set to store discovered script URLs.
        to_visit (list): List of URLs to be visited.
        visited (set): Set of already visited URLs.
        depth (int): The current depth of the crawl.
    """
    for script in soup.find_all('script', src=True):
        script_url = urljoin(base_url, script.get('src'))
        if script_url not in visited:
            discovered_urls.add(script_url)
            to_visit.append((script_url, depth + 1))

def check_meta_refresh(soup, base_url, discovered_urls, to_visit, visited, depth):
    """
    Checks for meta refresh tags and adds the redirect URL to the crawl queue.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
        base_url (str): The base URL for resolving redirect URLs.
        discovered_urls (set): Set to store discovered redirect URLs.
        to_visit (list): List of URLs to be visited.
        visited (set): Set of already visited URLs.
        depth (int): The current depth of the crawl.
    """
    meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if meta_refresh and 'content' in meta_refresh.attrs:
        content = meta_refresh['content']
        url_part = content.split('url=')[-1]
        refresh_url = urljoin(base_url, url_part.strip())
        if refresh_url not in visited:
            discovered_urls.add(refresh_url)
            to_visit.append((refresh_url, depth + 1))
