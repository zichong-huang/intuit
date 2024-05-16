import unittest
import json
import sys
import os

# Add the src directory to the system path to import lambda_function
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from lambda_function import lambda_handler, set_items

def make_request(method, operation, item=None):
    """General helper function for simulating Lambda events."""
    headers = {'Content-Type': 'application/json'}
    event = {
        "httpMethod": method,
        "body": json.dumps({"operation": operation, "item": item}) if method == "POST" else None,
        "queryStringParameters": {"operation": operation, "item": str(item)} if method in ["GET", "DELETE"] else None,
        "headers": headers
    }
    context = {}
    return lambda_handler(event, context)

class TestLocalLambda(unittest.TestCase):

    def setUp(self):
        """Reset the set_items before each test."""
        global set_items
        set_items.clear()

    def test_add_and_check_items(self):
        """Test: Add 1, 2, 3 into empty set, then check 1, 2, 3 are there."""
        print("\nRunning test: Add and Check Items")
        items = [1, 2, 3]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")
        
        # Check the items in the set
        for item in items:
            response = make_request('GET', "HasItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to check item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_items(self):
        """Test: Add 1, 2, 3 into empty set, then remove 2, check 1 and 3 are there."""
        print("\nRunning test: Add, Remove, and Check Items")
        items = [1, 2, 3]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")

        # Remove item 2
        response = make_request('DELETE', "RemoveItem", 2)
        self.assertEqual(response['statusCode'], 200, f"Failed to remove item 2: {response['body']}")
        response_data = json.loads(response['body'])
        self.assertIn('Item 2 removed successfully', response_data['message'])

        # Check the remaining items in the set
        remaining_items = [1, 3]
        for item in remaining_items:
            response = make_request('GET', "HasItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to check item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_item_absence(self):
        """Test: Add 1, 2, 3 into empty set, then remove 2, check 1 and 3 are there, remove 3, check 1 is there."""
        print("\nRunning test: Add, Remove, and Check Item Absence")
        items = [1, 2, 3]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")

        # Remove item 2
        response = make_request('DELETE', "RemoveItem", 2)
        self.assertEqual(response['statusCode'], 200, f"Failed to remove item 2: {response['body']}")
        response_data = json.loads(response['body'])
        self.assertIn('Item 2 removed successfully', response_data['message'])

        # Check remaining items in the set (1 and 3)
        remaining_items = [1, 3]
        for item in remaining_items:
            response = make_request('GET', "HasItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to check item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

        # Remove item 3
        response = make_request('DELETE', "RemoveItem", 3)
        self.assertEqual(response['statusCode'], 200, f"Failed to remove item 3: {response['body']}")
        response_data = json.loads(response['body'])
        self.assertIn('Item 3 removed successfully', response_data['message'])

        # Check remaining item in the set (only 1)
        response = make_request('GET', "HasItem", 1)
        self.assertEqual(response['statusCode'], 200, f"Failed to check item 1: {response['body']}")
        response_data = json.loads(response['body'])
        expected_message = f"Item 1 exists: True."
        self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item 1: {response_data}")

if __name__ == '__main__':
    unittest.main()
