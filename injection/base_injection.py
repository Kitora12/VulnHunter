from abc import ABC, abstractmethod
from colorama import Fore

class InjectionBase(ABC):
    def __init__(self, name):
        """
        Initializes the base class for injection types with a specified name.

        Args:
            name (str): The name of the injection type.
        """
        self.name = name
    
    @abstractmethod
    async def injection(self, form, url, client):
        """
        Abstract method for testing injection on a form. Must be implemented by subclasses.

        Args:
            form (bs4.element.Tag): The HTML form to be tested.
            url (str): The URL to which the form will be submitted.
            client (httpx.AsyncClient): The HTTP client used to send requests.

        Returns:
            None
        """
        pass
    
    def prepare_form_data(self, form, payload):
        """
        Prepares form data by injecting the specified payload into each input field.

        Args:
            form (bs4.element.Tag): The HTML form element containing input fields.
            payload (str): The payload to inject into the form fields.

        Returns:
            dict: A dictionary representing the prepared form data with payloads.
        """
        form_data = {}
        inputs = form.find_all('input')

        for input_tag in inputs:
            if input_tag.get('name'):
                form_data[input_tag.get('name')] = payload
        
        print(Fore.YELLOW + f"Form data prepared with payload: {payload}")
        return form_data
    
    async def send_injection_request(self, client, url, form_data):
        """
        Sends an HTTP POST request with the provided form data to test for injection.

        Args:
            client (httpx.AsyncClient): The HTTP client used to send the request.
            url (str): The URL to which the form data will be submitted.
            form_data (dict): The form data to include in the POST request.

        Returns:
            httpx.Response or None: The server's response to the injection request, or None if an error occurs.
        """
        try:
            response = await client.post(url, data=form_data)
            return response
        except Exception as e:
            print(Fore.RED + f"Error sending request to {url}: {e}")
            return None
