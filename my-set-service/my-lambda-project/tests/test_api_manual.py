import requests
import json

# Base URL of the API Gateway
BASE_URL = "https://lyz9wufcbk.execute-api.us-east-1.amazonaws.com/prod/"

# Headers
headers = {
    "Content-Type": "application/json"
}

# Function to add an item
def add_item(item):
    url = f"{BASE_URL}addItem"
    payload = {
        "operation": "AddItem",
        "item": item
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Add Item Response: {response.status_code}, {response.json()}")

# Function to remove an item
def remove_item(item):
    url = f"{BASE_URL}removeItem"
    payload = {
        "operation": "RemoveItem",
        "item": item
    }
    response = requests.delete(url, headers=headers, data=json.dumps(payload))
    print(f"Remove Item Response: {response.status_code}, {response.json()}")

# Function to check if an item exists
def has_item(item):
    url = f"{BASE_URL}hasItem"
    payload = {
        "operation": "HasItem",
        "item": item
    }
    response = requests.get(url, headers=headers, params=payload)
    print(f"Has Item Response: {response.status_code}, {response.json()}")

# Run multiple operations
def run_operations():
    items_to_add = [10, 20, 30]
    items_to_remove = [20]
    items_to_check = [10, 20, 30]

    # Add items
    for item in items_to_add:
        add_item(item)

    # Remove items
    for item in items_to_remove:
        remove_item(item)

    # Check items
    for item in items_to_check:
        has_item(item)

if __name__ == "__main__":
    run_operations()
