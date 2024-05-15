import unittest
import requests

def make_request(method, url, operation, item):
    """ General helper function for making HTTP requests. """
    headers = {'Content-Type': 'application/json'}
    params = {"operation": operation, "item": str(item)} if method == 'GET' else None
    data = {"operation": operation, "item": str(item)} if method in ["POST", "DELETE"] else None

    if method in ["POST", "DELETE"]:
        response = requests.request(method, url, json=data, headers=headers)
    elif method == "GET":
        response = requests.get(url, params=params, headers=headers)

    return response

class TestAPI(unittest.TestCase):
    base_url = "https://a541wh2ca6.execute-api.us-east-1.amazonaws.com/prod/"

    def test_add_and_check_items(self):
        """Test: Add 10, 20, 30 into empty set, then check the list is still the same after sorting."""
        print("\nRunning test: Add and Check Items")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', f"{self.base_url}addItem", "AddItem", item)
            self.assertTrue(response.ok, f"Failed to add item {item}: {response.text}")

        # Check the items in the set
        current_set = sorted(items)
        for item in current_set:
            response = make_request('GET', f"{self.base_url}hasItem", "HasItem", item)
            self.assertTrue(response.ok, f"Failed to check item {item}: {response.text}")
            response_data = response.json()
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_items(self):
        """Test: Add 10, 20, 30 into empty set, then remove 20, check the list contains only 10 and 30 after sorting."""
        print("\nRunning test: Add, Remove, and Check Items")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', f"{self.base_url}addItem", "AddItem", item)
            self.assertTrue(response.ok, f"Failed to add item {item}: {response.text}")

        # Remove item 20
        response = make_request('DELETE', f"{self.base_url}removeItem", "RemoveItem", 20)
        self.assertTrue(response.ok, f"Failed to remove item 20: {response.text}")

        # Check the remaining items in the set
        remaining_items = [10, 30]
        for item in remaining_items:
            response = make_request('GET', f"{self.base_url}hasItem", "HasItem", item)
            self.assertTrue(response.ok, f"Failed to check item {item}: {response.text}")
            response_data = response.json()
            expected_message = f"Item {item} exists: True."
            self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item {item}: {response_data}")

    def test_add_remove_and_check_item_absence(self):
        """Test: Add 10, 20, 30 into empty set, then remove 20, check if 20 is still there."""
        print("\nRunning test: Add, Remove, and Check Item Absence")
        items = [10, 20, 30]
        for item in items:
            response = make_request('POST', f"{self.base_url}addItem", "AddItem", item)
            self.assertTrue(response.ok, f"Failed to add item {item}: {response.text}")

        # Remove item 20
        response = make_request('DELETE', f"{self.base_url}removeItem", "RemoveItem", 20)
        self.assertTrue(response.ok, f"Failed to remove item 20: {response.text}")

        # Check that item 20 is not in the set
        response = make_request('GET', f"{self.base_url}hasItem", "HasItem", 20)
        self.assertTrue(response.ok, f"Failed to check item 20: {response.text}")
        response_data = response.json()
        expected_message = "Item 20 exists: False."
        self.assertEqual(response_data.get("message"), expected_message, f"Unexpected response for item 20: {response_data}")

if __name__ == '__main__':
    unittest.main()
