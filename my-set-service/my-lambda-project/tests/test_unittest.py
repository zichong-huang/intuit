import unittest
import json
import sys
import os

# Add the src directory to the system path to import lambda_function
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from lambda_function import lambda_handler

def make_request(method, operation, item):
    """ General helper function for simulating Lambda events. """
    headers = {'Content-Type': 'application/json'}
    event = {
        "httpMethod": method,
        "body": json.dumps({"operation": operation, "item": item}) if method in ["POST", "DELETE"] else None,
        "queryStringParameters": {"operation": operation, "item": str(item)} if method == "GET" else None,
        "headers": headers
    }
    context = {}
    return lambda_handler(event, context)

class TestLocalLambda(unittest.TestCase):

    def test_add_and_check_items(self):
        """Test: Add 10, 20, 30 into empty set, then check the list is still the same after sorting."""
        print("\nRunning test: Add and Check Items")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f'Item {item} added successfully. Current set: {items[:items.index(item) + 1]}'
            self.assertEqual(response_data['message'], expected_message, f"Unexpected response for item {item}: {response_data}")

        # Check the items in the set
        for item in sorted(items):
            response = make_request('GET', "HasItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to check item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_items(self):
        """Test: Add 10, 20, 30 into empty set, then remove 20, check the list contains only 10 and 30 after sorting."""
        print("\nRunning test: Add, Remove, and Check Items")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")
        
        # Remove item 20
        response = make_request('DELETE', "RemoveItem", 20)
        self.assertEqual(response['statusCode'], 200, f"Failed to remove item 20: {response['body']}")
        response_data = json.loads(response['body'])
        self.assertIn('Item 20 removed successfully', response_data['message'])

        # Check the remaining items in the set
        remaining_items = [10, 30]
        for item in remaining_items:
            response = make_request('GET', "HasItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to check item {item}: {response['body']}")
            response_data = json.loads(response['body'])
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_item_absence(self):
        """Test: Add 10, 20, 30 into empty set, then remove 20, check if 20 is still there."""
        print("\nRunning test: Add, Remove, and Check Item Absence")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', "AddItem", item)
            self.assertEqual(response['statusCode'], 200, f"Failed to add item {item}: {response['body']}")

        # Remove item 20
        response = make_request('DELETE', "RemoveItem", 20)
        self.assertEqual(response['statusCode'], 200, f"Failed to remove item 20: {response['body']}")
        response_data = json.loads(response['body'])
        self.assertIn('Item 20 removed successfully', response_data['message'])

        # Check that item 20 is not in the set
        response = make_request('GET', "HasItem", 20)
        self.assertEqual(response['statusCode'], 200, f"Failed to check item 20: {response['body']}")
        response_data = json.loads(response['body'])
        expected_message = "Item 20 exists: False."
        self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item 20: {response_data}")

if __name__ == '__main__':
    unittest.main()
