# VulnHunter

VulnHunter is a small educational project designed to detect common web vulnerabilities such as SQL Injection, XSS, and Command Injection. It crawls the website, tests forms and GET parameters, and generates a report on discovered vulnerabilities.

## Features

- **SQL Injection Detection**: Detects SQL injection vulnerabilities in GET parameters and form inputs.
- **XSS Injection Detection**: Detects Cross-Site Scripting (XSS) vulnerabilities in form inputs.
- **Command Injection Detection**: Detects command injection vulnerabilities in GET parameters and form inputs.
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
python3 main.py -u <URL> --sql --xss --command -r
```

- `-u <URL>`: The target URL for the scan.
- `--sql`: Enables SQL injection testing.
- `--xss`: Enables XSS testing.
- `--command`: Enables Command Injection testing.
- `-r`: Generates a report of the findings.

### Example

```bash
python3 main.py -u http://example.com --sql --xss --command -r
```

This command will scan the target URL for SQL Injection, XSS, and Command Injection vulnerabilities and generate a report.

### Testing GET Parameters

The tool also supports scanning GET parameters for vulnerabilities. For example:

```bash
python3 main.py -u http://example.com/search?q=test --sql
```

### Command Injection Detection

To test for command injection vulnerabilities, use the `--command` flag:

```bash
python3 main.py -u http://example.com/ping?ip=127.0.0.1 --command
```

This will test for command injection vulnerabilities in the `ip` parameter.

### SQL Injection Payloads

You can extend the SQL injection payloads by adding your own payloads in the `payloads/sql_payloads.txt` file. Each payload should be on a new line.

### XSS Injection Payloads

Similarly, XSS payloads can be extended by adding to the `payloads/xss_payloads.txt` file.

### Command Injection Payloads

Command injection payloads can be customized by adding new payloads in the `payloads/command_payloads.txt` file.

## Reports

When the `-r` flag is used, a report will be generated and saved in the `results` directory. The report will contain details about the vulnerabilities found, including the vulnerable URLs.

## Extending Payloads

To extend the tool’s capabilities, you can modify the following files:
- **SQL Payloads**: Add new SQL injection payloads in `payloads/sql_payloads.txt`.
- **XSS Payloads**: Add new XSS payloads in `payloads/xss_payloads.txt`.
- **Command Payloads**: Add new command injection payloads in `payloads/command_payloads.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
