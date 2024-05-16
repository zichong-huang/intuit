import unittest
import requests
import json

# Base URL of the API Gateway
BASE_URL = "https://7okw1aj4k2.execute-api.us-east-1.amazonaws.com/prod/"

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
    url = f"{BASE_URL}removeItem"
    params = {
        "item": item
    }
    response = requests.delete(url, headers=headers, params=params)
    return response

def has_item(item):
    url = f"{BASE_URL}hasItem"
    params = {
        "item": item
    }
    response = requests.get(url, headers=headers, params=params)
    return response

def reset_set():
    url = f"{BASE_URL}resetSet"
    payload = {
        "operation": "Reset"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response

class TestAPIGateway(unittest.TestCase):

    def setUp(self):
        """Reset the remote set_items before each test."""
        response = reset_set()
        self.assertEqual(response.status_code, 200)

    def test_add_and_check_items(self):
        """Test: Add 1, 2, 3 into empty set, then check 1, 2, 3 are there."""
        print("\nRunning test: Add and Check Items")
        items = [1, 2, 3]
        for item in items:
            response = add_item(item)
            self.assertEqual(response.status_code, 200)
        
        # Check the items in the set
        for item in items:
            response = has_item(item)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data['message'], expected_message)

    def test_add_remove_and_check_items(self):
        """Test: Add 1, 2, 3 into empty set, then remove 2, check 1 and 3 are there."""
        print("\nRunning test: Add, Remove, and Check Items")
        items = [1, 2, 3]
        for item in items:
            response = add_item(item)
            self.assertEqual(response.status_code, 200)

        # Remove item 2
        response = remove_item(2)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('Item 2 removed successfully', response_data['message'])

        # Check the remaining items in the set
        remaining_items = [1, 3]
        for item in remaining_items:
            response = has_item(item)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data['message'], expected_message)

    def test_add_remove_and_check_item_absence(self):
        """Test: Add 1, 2, 3 into empty set, then remove 2, check 1 and 3 are there, remove 3, check 1 is there."""
        print("\nRunning test: Add, Remove, and Check Item Absence")
        items = [1, 2, 3]
        for item in items:
            response = add_item(item)
            self.assertEqual(response.status_code, 200)

        # Remove item 2
        response = remove_item(2)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('Item 2 removed successfully', response_data['message'])

        # Check remaining items in the set (1 and 3)
        remaining_items = [1, 3]
        for item in remaining_items:
            response = has_item(item)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data['message'], expected_message)

        # Remove item 3
        response = remove_item(3)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('Item 3 removed successfully', response_data['message'])

        # Check remaining item in the set (only 1)
        response = has_item(1)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_message = f"Item 1 exists: True."
        self.assertEqual(response_data['message'], expected_message)

if __name__ == '__main__':
    unittest.main()
