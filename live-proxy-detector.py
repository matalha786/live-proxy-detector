import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to read proxies from a file
def read_proxies(file_name):
    try:
        with open(file_name, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []

# Function to check if a proxy is alive
def check_proxy(proxy):
    test_url = "http://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=7)
        if response.status_code == 200:
            print(f"Proxy {proxy} is alive")
            with open('live.txt', 'a') as live_file:
                live_file.write(proxy + '\n')
            return proxy, "alive"
    except requests.RequestException:
        pass
    print(f"Proxy {proxy} is dead")
    return proxy, "dead"

# Function to check all proxies in the list
def check_proxies(proxies, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check_proxy, proxies))
    return results

# Main function
if __name__ == "__main__":
    file_name = input("Enter the name of the file containing the proxies: ")
    proxies = read_proxies(file_name)
    
    max_workers = 32  # 8 cores * 4 threads per core

    if proxies:
        proxy_results = check_proxies(proxies, max_workers)
        print("\nSummary:")
        for proxy, status in proxy_results:
            print(f"{proxy} is {status}")
