from abc import ABC, abstractmethod
from colorama import Fore

class InjectionBase(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    async def injection(self, form, url, client):
        pass
    
    def prepare_form_data(self, form, payload):
        form_data = {}
        inputs = form.find_all('input')

        for input_tag in inputs:
            if input_tag.get('name'):
                form_data[input_tag.get('name')] = payload
        
        print(Fore.YELLOW + f"Form data prepared with payload: {payload}")
        return form_data
    
    async def send_injection_request(self, client, url, form_data):
        try:
            response = await client.post(url, data=form_data)
            return response
        except Exception as e:
            print(Fore.RED + f"Error sending request to {url}: {e}")
            return None
