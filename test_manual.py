import requests
import json

BASE_URL = "http://localhost:5000"

def test_home():
    print("\n=== Testing Home Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(json.dumps(response.json(), indent=2))

def test_status():
    print("\n=== Checking Current Status ===")
    response = requests.get(f"{BASE_URL}/status")
    print(json.dumps(response.json(), indent=2))

def test_unsafe_increment():
    print("\n=== Testing Unsafe Increment ===")
    response = requests.post(f"{BASE_URL}/increment")
    print(json.dumps(response.json(), indent=2))

def test_safe_increment():
    print("\n=== Testing Safe Increment ===")
    response = requests.post(f"{BASE_URL}/increment-safe")
    print(json.dumps(response.json(), indent=2))

def test_reset():
    print("\n=== Resetting Counters ===")
    response = requests.post(f"{BASE_URL}/reset")
    print(json.dumps(response.json(), indent=2))

def main():
    print("REST-based Distributed Counter - Manual Testing")
    print("=" * 50)
    
    try:
        # Test all endpoints
        test_home()
        test_reset()
        test_status()
        
        print("\n--- Making 5 unsafe increments ---")
        for i in range(5):
            test_unsafe_increment()
        
        print("\n--- Making 5 safe increments ---")
        for i in range(5):
            test_safe_increment()
        
        test_status()
        
        print("\n✓ All manual tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to server.")
        print("Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    main()