import os
import requests
import argparse
import time
import threading
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

# Function to save the progress
def save_progress(proxies, file_name='progress.txt'):
    with open(file_name, 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')

# Function to load the progress
def load_progress(file_name='progress.txt'):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    return []

# Function to check if a proxy is alive
def check_proxy(proxy):
    test_url = "http://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=7)
        if response.status_code == 200:
            with open('live.txt', 'a') as live_file:
                live_file.write(proxy + '\n')
            return proxy, "alive"
    except requests.RequestException:
        pass
    return proxy, "dead"

# Function to check all proxies in the list
def check_proxies(proxies, max_workers, progress_tracker):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(progress_tracker, proxies))
    return results

# Function to check internet connection
def check_internet(url='http://www.google.com', timeout=7):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

# Function to track and print progress
def track_progress(total_proxies, completed_proxies):
    while True:
        time.sleep(10)
        progress = (completed_proxies[0] / total_proxies) * 100
        print(f"\n \n Progress: {progress:.2f}%")
        print(f"\n \n Progress: {progress:.2f}%")
        print(f"\n \n Progress: {progress:.2f}%")
# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check proxies from a file.')
    parser.add_argument('file', metavar='filename', type=str, help='Path to the file containing proxies')
    args = parser.parse_args()

    file_name = args.file
    proxies = read_proxies(file_name)
    
    # Load progress if available
    progress_file = 'progress.txt'
    remaining_proxies = load_progress(progress_file) or proxies
    
    max_workers = 1024  # 8 cores * 8 threads per core

    if remaining_proxies:
        total_proxies = len(remaining_proxies)
        completed_proxies = [0]
        
        # Start the progress tracking thread
        progress_thread = threading.Thread(target=track_progress, args=(total_proxies, completed_proxies))
        progress_thread.daemon = True
        progress_thread.start()
        
        # Define a wrapper to update completed proxies count and print live/dead status
        def progress_tracker(proxy):
            result = check_proxy(proxy)
            completed_proxies[0] += 1
            print(f"Proxy {proxy} is {result[1]}")
            return result
        
        while remaining_proxies:
            if check_internet():
                proxy_results = check_proxies(remaining_proxies, max_workers, progress_tracker)
                remaining_proxies = [proxy for proxy, status in proxy_results if status == "dead"]
                save_progress(remaining_proxies, progress_file)
                break  # No need to print summary anymore
            else:
                print("\nInternet connection is disconnected. Please check your connection and restart the program.")
                time.sleep(10)  # Wait for 10 seconds before rechecking the connection
        
        # Delete progress file after completion
        if os.path.exists(progress_file):
            os.remove(progress_file)
