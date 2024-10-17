import httpx
from bs4 import BeautifulSoup
from colorama import Fore

async def crawl_site(url):
    print(Fore.YELLOW + f"Crawling the website: {url}...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                print(Fore.RED + f"Failed to retrieve {url}, Status Code: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            if forms:
                print(Fore.GREEN + f"Found {len(forms)} forms.")
            else:
                print(Fore.RED + "No forms found.")
                
            return forms
        except Exception as e:
            print(Fore.RED + f"Error during crawling: {e}")
            return []
