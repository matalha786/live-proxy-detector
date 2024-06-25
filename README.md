# live-proxy-detector
# Proxy Checker

This Python script checks a list of proxies from a file, using user agents to avoid detection by websites. It concurrently checks the proxies and saves live proxies to a `live.txt` file.

## Features

- **Proxy Checking**: Concurrently checks proxies from a specified file.
- **Multithreading**: Utilizes `ThreadPoolExecutor` for efficient concurrent processing.
- **Timeout Handling**: Sets a timeout for each proxy check to manage network latency.

## Requirements

- Python 3.x
- `requests` library: Install using `pip install requests`

## Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/proxy-checker.git
   cd proxy-checker
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Proxies File**:

   Create a text file (`proxies.txt`) with one proxy per line in the format `http://ip:port`.

4. **Run the Script**:

   ```bash
   python proxy_checker.py
   ```

   - Enter the filename when prompted (e.g., `proxies.txt`).
   - The script will check each proxy using user agents, save live proxies to `live.txt`, and print the status of each proxy.

5. **Customization**:

   - Adjust `max_workers` in `proxy_checker.py` based on your system's capabilities.
   - Modify the timeout (`timeout=7`) in the `check_proxy` function for different network conditions.

## Notes

- Make sure your proxies are reliable and accessible from your network.
- Use responsibly and respect website policies regarding proxy usage and scraping.

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.
