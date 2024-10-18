from injection.base_injection import InjectionBase
from colorama import Fore
from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup

class XSSInjection(InjectionBase):
    def __init__(self):
        super().__init__("XSS Injection")

    def load_xss_payloads(self, filepath="payloads/xss_payloads.txt"):
        """
        Loads XSS payloads from the specified file.

        Args:
            filepath (str): Path to the file containing XSS payloads.

        Returns:
            list: A list of XSS payloads.
        """
        try:
            with open(filepath, 'r') as file:
                payloads = [line.strip() for line in file.readlines()]
            print(Fore.GREEN + f"Loaded {len(payloads)} XSS payloads from {filepath}")
            return payloads
        except Exception as e:
            print(Fore.RED + f"Error loading payloads from {filepath}: {e}")
            return []

    async def injection(self, forms, url, client):
        """
        Tests each form for XSS vulnerabilities using a set of payloads.

        Args:
            forms (list): List of HTML form elements to test.
            url (str): The base URL to use for testing.
            client (httpx.AsyncClient): The HTTP client to make requests.

        Returns:
            list: A list of detected XSS vulnerabilities, each as a tuple of the vulnerable URL and payload.
        """
        print(Fore.CYAN + f"Testing for {self.name} on {url}...")

        xss_payloads = self.load_xss_payloads()
        vulnerabilities = []

        for form in forms:
            if not hasattr(form, 'get'):
                print(Fore.RED + "Skipping non-form element.")
                continue

            action = form.get('action', '')
            full_url = url + action if action else url

            for payload in xss_payloads:
                form_data = self.prepare_form_data(form, payload)

                response = await self.send_injection_request(client, full_url, form_data)
                if response and payload in response.text:
                    print(Fore.RED + f"XSS vulnerability found at {full_url} with payload: {payload}")
                    vulnerabilities.append((full_url, payload))

                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if payload in str(soup):
                        print(Fore.RED + f"Persistent XSS vulnerability detected at {full_url} with payload: {payload}")
                        vulnerabilities.append((full_url, payload))

        if not vulnerabilities:
            print(Fore.GREEN + "No XSS vulnerabilities found.")

        return vulnerabilities

    async def test_xss_on_get_params(self, url, client):
        """
        Tests GET parameters of a URL for XSS vulnerabilities using a set of payloads.

        Args:
            url (str): The URL with query parameters to test for XSS.
            client (httpx.AsyncClient): The HTTP client to make requests.

        Returns:
            list: A list of detected XSS vulnerabilities, each as a tuple of the vulnerable URL and payload.
        """
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
                    print(Fore.RED + f"XSS vulnerability found at {new_url} with payload: {payload}")
                    vulnerabilities.append((new_url, payload))

        if not vulnerabilities:
            print(Fore.GREEN + "No XSS vulnerabilities found in GET parameters.")

        return vulnerabilities
