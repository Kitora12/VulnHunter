# VulnHunter

VulnHunter is a small educational project designed to detect common web vulnerabilities such as SQL Injection and XSS. It crawls the website, tests forms and GET parameters, and generates a report on discovered vulnerabilities.

## Features

- **SQL Injection Detection**: Detects SQL injection vulnerabilities in GET parameters and form inputs.
- **XSS Injection Detection**: Detects Cross-Site Scripting (XSS) vulnerabilities in form inputs.
- **Automated Crawling**: Automatically crawls the website to identify forms and fields to test.
- **Report Generation**: Generates a detailed report with the discovered vulnerabilities.

## Prerequisites

- Python 3.x
- `httpx`, `beautifulsoup4`, `colorama`, `asyncio`

You can install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

You can run the scanner with the following command:

```bash
python3 main.py -u <URL> --sql --xss -r
```

- `-u <URL>`: The target URL for the scan.
- `--sql`: Enables SQL injection testing.
- `--xss`: Enables XSS testing.
- `-r`: Generates a report of the findings.

### Example

```bash
python3 main.py -u http://example.com --sql --xss -r
```

This command will scan the target URL for SQL Injection and XSS vulnerabilities and generate a report.

### Testing GET Parameters

The tool also supports scanning GET parameters for vulnerabilities. For example:

```bash
python3 main.py -u http://example.com/search?q=test --sql
```

### SQL Injection Payloads

You can extend the SQL injection payloads by adding your own payloads in the `payloads/sql_payloads.txt` file. Each payload should be on a new line.

### XSS Injection Payloads

Similarly, XSS payloads can be extended by adding to the `payloads/xss_payloads.txt` file.

## Reports

When the `-r` flag is used, a report will be generated and saved in the `results` directory. The report will contain details about the vulnerabilities found, including the vulnerable URLs.

## Extending Payloads

To extend the tool’s capabilities, you can modify the following files:
- **SQL Payloads**: Add new SQL injection payloads in `payloads/sql_payloads.txt`.
- **XSS Payloads**: Add new XSS payloads in `payloads/xss_payloads.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
