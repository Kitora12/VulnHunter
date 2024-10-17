import argparse
from colorama import Fore

def parse_arguments():
    print(Fore.YELLOW + "Parsing command-line arguments...")

    parser = argparse.ArgumentParser(description="Web Vulnerability Scanner")
    
    parser.add_argument('-u', '--url', type=str, required=True, help="Target website URL to scan")
    parser.add_argument('--sql', action='store_true', help="Enable SQL Injection testing")
    parser.add_argument('--xss', action='store_true', help="Enable XSS Injection testing")
    parser.add_argument('-r', '--report', action='store_true', help="Generate a report of the findings")
    
    args = parser.parse_args()
    print(Fore.GREEN + "Arguments parsed successfully.")
    
    return args
