from injection.base_injection import InjectionBase
from colorama import Fore
from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup

class XSSInjection(InjectionBase):
    def __init__(self):
        super().__init__("XSS Injection")

    def load_xss_payloads(self, filepath="payloads/xss_payloads.txt"):
        try:
            with open(filepath, 'r') as file:
                payloads = [line.strip() for line in file.readlines()]
            print(Fore.GREEN + f"Loaded {len(payloads)} XSS payloads from {filepath}")
            return payloads
        except Exception as e:
            print(Fore.RED + f"Error loading payloads from {filepath}: {e}")
            return []

    async def injection(self, form, url, client):
        print(Fore.CYAN + f"Testing for {self.name} on {url}...")
        
        xss_payloads = self.load_xss_payloads()
        vulnerabilities = []
        action = form.get('action')
        full_url = url + action if action else url

        for payload in xss_payloads:
            form_data = self.prepare_form_data(form, payload)

            response = await self.send_injection_request(client, full_url, form_data)
            if response and payload in response.text:
                print(Fore.RED + f"XSS vulnerability found at {full_url}")
                vulnerabilities.append(full_url)

            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                if payload in str(soup):
                    print(Fore.RED + f"Persistente XSS vulnerability detected at {full_url}")
                    vulnerabilities.append(full_url)

        if not vulnerabilities:
            print(Fore.GREEN + "No XSS vulnerabilities found.")

        return vulnerabilities

    async def test_xss_on_get_params(self, url, client):
        print(Fore.CYAN + f"Testing GET parameters for XSS on {url}...")

        xss_payloads = self.load_xss_payloads()
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if not query_params:
            print(Fore.RED + "No GET parameters found.")
            return []

        vulnerabilities = []

        for param in query_params:
            for payload in xss_payloads:
                new_query_params = query_params.copy()
                new_query_params[param] = payload
                new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(new_query_params, doseq=True)}"
                
                response = await client.get(new_url)
                if payload in response.text:
                    print(Fore.RED + f"XSS vulnerability found at {new_url}")
                    vulnerabilities.append(new_url)

        if not vulnerabilities:
            print(Fore.GREEN + "No XSS vulnerabilities found in GET parameters.")

        return vulnerabilities
