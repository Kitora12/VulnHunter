from injection.base_injection import InjectionBase
from colorama import Fore
from urllib.parse import urlparse, parse_qs, urlencode
import httpx

class SQLInjection(InjectionBase):
    def __init__(self):
        """
        Initializes the SQLInjection class with a name for the injection type.
        """
        super().__init__("SQL Injection")

    def load_sql_payloads(self, filepath="payloads/sql_payloads.txt"):
        """
        Loads SQL injection payloads from the specified file.

        Args:
            filepath (str): Path to the file containing SQL injection payloads.

        Returns:
            list: A list of SQL injection payloads.
        """
        try:
            with open(filepath, 'r') as file:
                payloads = [line.strip() for line in file.readlines()]
            print(Fore.GREEN + f"Loaded {len(payloads)} SQL payloads from {filepath}")
            return payloads
        except Exception as e:
            print(Fore.RED + f"Error loading payloads from {filepath}: {e}")
            return []

    async def injection(self, forms, url, client):
        """
        Tests each form for SQL injection vulnerabilities using a set of payloads.

        Args:
            forms (list): List of HTML form elements to test.
            url (str): The base URL to use for testing.
            client (httpx.AsyncClient): The HTTP client to make requests.

        Returns:
            list: A list of detected SQL injection vulnerabilities, each as a tuple of the vulnerable URL and payload.
        """
        print(Fore.CYAN + f"Testing for {self.name} on {url}...")
        
        sql_payloads = self.load_sql_payloads()
        vulnerabilities = []

        for form in forms:
            if not hasattr(form, 'get'):
                print(Fore.RED + "Skipping non-form element.")
                continue

            action = form.get('action', '')
            full_url = url + action if action else url

            for payload in sql_payloads:
                form_data = self.prepare_form_data(form, payload)
                response = await self.send_injection_request(client, full_url, form_data)

                if response and ("syntax error" in response.text.lower() or "mysql" in response.text.lower()):
                    print(Fore.RED + f"SQL Injection vulnerability found at {full_url} with payload: {payload}")
                    vulnerabilities.append((full_url, payload))

        if not vulnerabilities:
            print(Fore.GREEN + "No SQL Injection vulnerabilities found.")

        return vulnerabilities

    async def test_sql_injection_on_get_params(self, url, client):
        """
        Tests GET parameters of a URL for SQL injection vulnerabilities using a set of payloads.

        Args:
            url (str): The URL with query parameters to test for SQL injection.
            client (httpx.AsyncClient): The HTTP client to make requests.

        Returns:
            list: A list of detected SQL injection vulnerabilities, each as a tuple of the vulnerable URL and payload.
        """
        print(Fore.CYAN + f"Testing GET parameters for SQL Injection on {url}...")

        sql_payloads = self.load_sql_payloads()
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if not query_params:
            print(Fore.RED + "No GET parameters found.")
            return []

        vulnerabilities = []

        for param in query_params:
            for payload in sql_payloads:
                new_query_params = query_params.copy()
                new_query_params[param] = payload
                new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(new_query_params, doseq=True)}"

                try:
                    response = await client.get(new_url, timeout=5)
                    if "syntax error" in response.text.lower() or "mysql" in response.text.lower():
                        print(Fore.RED + f"SQL Injection vulnerability found at {new_url} with payload: {payload}")
                        vulnerabilities.append(new_url)
                except httpx.ReadTimeout:
                    print(Fore.YELLOW + f"Timeout occurred while testing payload on {new_url}. Skipping...")
                except Exception as e:
                    print(Fore.RED + f"Error while testing payload on {new_url}: {e}")

        if not vulnerabilities:
            print(Fore.GREEN + "No SQL Injection vulnerabilities found in GET parameters.")

        return vulnerabilities
