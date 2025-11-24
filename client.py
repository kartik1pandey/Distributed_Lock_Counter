import requests
import threading
import time
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = "http://localhost:5000"

def reset_counters():
    """Reset both counters before test"""
    try:
        response = requests.post(f"{BASE_URL}/reset")
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ Counters reset{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}✗ Error resetting: {e}{Style.RESET_ALL}")

def increment_counter(endpoint, thread_id, results):
    """Make increment request"""
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            data = response.json()
            results.append(data['counter'])
    except Exception as e:
        print(f"{Fore.RED}Thread {thread_id} error: {e}{Style.RESET_ALL}")

def run_concurrent_test(endpoint, num_threads):
    """Run concurrent increment test"""
    threads = []
    results = []
    
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_counter,
            args=(endpoint, i, results)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results

def get_final_status():
    """Get final counter values"""
    try:
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"{Fore.RED}Error getting status: {e}{Style.RESET_ALL}")
    return None

def main():
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  DISTRIBUTED COUNTER - CONCURRENCY CONTROL DEMO")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    # Test configuration
    NUM_REQUESTS = 100
    
    print(f"{Fore.YELLOW}Test Configuration:{Style.RESET_ALL}")
    print(f"  • Number of concurrent requests: {NUM_REQUESTS}")
    print(f"  • Each request increments counter by 1")
    print(f"  • Expected final value: {NUM_REQUESTS}\n")
    
    # Test 1: Without Lock (Unsafe)
    print(f"{Fore.MAGENTA}{'─'*60}")
    print(f"TEST 1: INCREMENT WITHOUT LOCK (UNSAFE)")
    print(f"{'─'*60}{Style.RESET_ALL}")
    
    reset_counters()
    print(f"{Fore.YELLOW}Running {NUM_REQUESTS} concurrent unsafe increments...{Style.RESET_ALL}")
    
    start_time = time.time()
    run_concurrent_test("increment", NUM_REQUESTS)
    elapsed = time.time() - start_time
    
    status = get_final_status()
    if status:
        unsafe_value = status['unsafe_counter']
        lost_updates = NUM_REQUESTS - unsafe_value
        
        print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
        print(f"  Expected value: {Fore.GREEN}{NUM_REQUESTS}{Style.RESET_ALL}")
        print(f"  Actual value:   {Fore.RED}{unsafe_value}{Style.RESET_ALL}")
        print(f"  Lost updates:   {Fore.RED}{lost_updates}{Style.RESET_ALL}")
        print(f"  Time taken:     {elapsed:.3f}s")
        
        if lost_updates > 0:
            print(f"\n  {Fore.RED}⚠ LOST UPDATE PROBLEM DETECTED!{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Race condition caused {lost_updates} updates to be lost{Style.RESET_ALL}")
    
    # Wait before next test
    time.sleep(1)
    
    # Test 2: With Lock (Safe)
    print(f"\n{Fore.MAGENTA}{'─'*60}")
    print(f"TEST 2: INCREMENT WITH LOCK (SAFE)")
    print(f"{'─'*60}{Style.RESET_ALL}")
    
    reset_counters()
    print(f"{Fore.YELLOW}Running {NUM_REQUESTS} concurrent safe increments...{Style.RESET_ALL}")
    
    start_time = time.time()
    run_concurrent_test("increment-safe", NUM_REQUESTS)
    elapsed = time.time() - start_time
    
    status = get_final_status()
    if status:
        safe_value = status['safe_counter']
        
        print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
        print(f"  Expected value: {Fore.GREEN}{NUM_REQUESTS}{Style.RESET_ALL}")
        print(f"  Actual value:   {Fore.GREEN}{safe_value}{Style.RESET_ALL}")
        print(f"  Lost updates:   {Fore.GREEN}0{Style.RESET_ALL}")
        print(f"  Time taken:     {elapsed:.3f}s")
        
        if safe_value == NUM_REQUESTS:
            print(f"\n  {Fore.GREEN}✓ SUCCESS! Lock prevented race conditions{Style.RESET_ALL}")
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Key Takeaway:{Style.RESET_ALL}")
    print(f"  Without locking, concurrent access causes lost updates.")
    print(f"  With locking, all updates are correctly applied.")
    print(f"\n{Fore.GREEN}Demo completed!{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")