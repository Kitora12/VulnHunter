from datetime import datetime
from colorama import Fore

def generate_report(vuln_sites, filename=None):
    if not filename:
        filename = f"report_{datetime.now().strftime('%Y-%m-%d')}.txt"
    
    print(Fore.YELLOW + f"Generating report: {filename}...")

    with open(f"results/{filename}", "w") as report_file:
        report_file.write("Vulnerability Scan Report\n")
        report_file.write("=========================\n\n")
        if vuln_sites:
            report_file.write("Vulnerabilities detected on the following URLs:\n")
            for site in vuln_sites:
                report_file.write(f"- {site}\n")
        else:
            report_file.write("No vulnerabilities detected.")
    
    print(Fore.GREEN + f"Report saved: results/{filename}")
