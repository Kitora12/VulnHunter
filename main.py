import asyncio
from colorama import init, Fore, Style
from scanner.crawler import crawl_site
from utils.report_generator import generate_report
from injection.sql_injection import SQLInjection
from injection.xss_injection import XSSInjection
from scanner.args_parser import parse_arguments
import httpx
from injection.command_injection import CommandInjection

init(autoreset=True)

async def scan_website(url, test_sql, test_xss, test_command):
    print(Fore.YELLOW + Style.BRIGHT + f"Scanning website: {url}...")

    forms = await crawl_site(url)
    vulnerabilities_found = []

    async with httpx.AsyncClient() as client:
        if test_sql:
            print(Fore.CYAN + "Testing for SQL Injections...")
            sql_tester = SQLInjection()
            
            get_vulns = await sql_tester.test_sql_injection_on_get_params(url, client)
            vulnerabilities_found.extend(get_vulns)
            
            if forms:
                for form in forms:
                    sql_vulns = await sql_tester.injection(form, url, client)
                    if sql_vulns:
                        vulnerabilities_found.extend(sql_vulns)
                        print(Fore.RED + f"SQL Injection vulnerabilities found: {sql_vulns}")

        if test_xss:
            print(Fore.CYAN + "Testing for XSS Injections...")
            xss_tester = XSSInjection()
            for form in forms:
                xss_vulns = await xss_tester.injection(form, url, client)
                if xss_vulns:
                    vulnerabilities_found.extend(xss_vulns)
                    print(Fore.RED + f"XSS Injection vulnerabilities found: {xss_vulns}")

        if test_command:
            print(Fore.CYAN + "Testing for Command Injections...")
            command_tester = CommandInjection()

            command_vulns = await command_tester.test_command_injection_on_get_params(url, client)
            vulnerabilities_found.extend(command_vulns)

            if forms:
                for form in forms:
                    form_command_vulns = await command_tester.injection(form, url, client)
                    if form_command_vulns:
                        vulnerabilities_found.extend(form_command_vulns)
                        print(Fore.RED + f"Command Injection vulnerabilities found: {form_command_vulns}")

    return vulnerabilities_found


def main():
    args = parse_arguments()

    vulnerabilities = asyncio.run(scan_website(args.url, args.sql, args.xss, args.command))

    if vulnerabilities:
        print(Fore.GREEN + Style.BRIGHT + f"Vulnerabilities found: {vulnerabilities}")
    else:
        print(Fore.GREEN + Style.BRIGHT + "No vulnerabilities detected.")

    if args.report:
        generate_report(vulnerabilities)
        print(Fore.YELLOW + "Report generated.")

if __name__ == "__main__":
    main()
