import unittest
import requests
import json

# Base URL of the API Gateway
BASE_URL = "https://lyz9wufcbk.execute-api.us-east-1.amazonaws.com/prod/"

# Headers
headers = {
    "Content-Type": "application/json"
}

def add_item(item):
    url = f"{BASE_URL}addItem"
    payload = {
        "operation": "AddItem",
        "item": item
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response

def remove_item(item):
    url = f"{BASE_URL}removeItem?operation=RemoveItem&item={item}"
    response = requests.delete(url, headers=headers)
    return response

def has_item(item):
    url = f"{BASE_URL}hasItem"
    params = {
        "operation": "HasItem",
        "item": item
    }
    response = requests.get(url, headers=headers, params=params)
    return response

class TestAPIGateway(unittest.TestCase):
    def test_add_item(self):
        """Test adding an item to the set."""
        item = 10
        response = add_item(item)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f'Item {item} added successfully. Current set: [{item}]'
        self.assertEqual(response_data['message'], expected_message)

    def test_add_existing_item(self):
        """Test adding an existing item to the set."""
        item = 10
        add_item(item)  # Add item initially
        response = add_item(item)  # Try adding the same item again
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f'Item {item} already exists in the set. No action taken.'
        self.assertEqual(response_data['message'], expected_message)

    def test_remove_item(self):
        """Test removing an item from the set."""
        item = 10
        add_item(item)  # Ensure item is added first
        response = remove_item(item)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f'Item {item} removed successfully. Current set: []'
        self.assertEqual(response_data['message'], expected_message)

    def test_remove_nonexistent_item(self):
        """Test removing an item that does not exist in the set."""
        item = 20
        response = remove_item(item)
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        expected_message = f'Item {item} not found in the set.'
        self.assertEqual(response_data['message'], expected_message)

    def test_has_item(self):
        """Test checking if an item exists in the set."""
        item = 10
        add_item(item)  # Ensure item is added first
        response = has_item(item)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f"Item {item} exists: True."
        self.assertEqual(response_data['message'], expected_message)

    def test_item_not_exists(self):
        """Test checking if an item that does not exist in the set."""
        item = 20
        response = has_item(item)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f"Item {item} exists: False."
        self.assertEqual(response_data['message'], expected_message)

if __name__ == '__main__':
    unittest.main()
