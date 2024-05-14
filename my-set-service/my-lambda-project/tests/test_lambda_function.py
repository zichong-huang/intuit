import unittest
from src.lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        # Setup a known environment if necessary
        self.test_events = {
            'add': {'operation': 'AddItem', 'item': '10'},
            'remove': {'operation': 'RemoveItem', 'item': '10'},
            'has': {'operation': 'HasItem', 'item': '10'},
            'bad_request': {'operation': 'BadOperation', 'item': '10'},
            'non_int': {'operation': 'AddItem', 'item': 'ten'}
        }

    def test_add_item(self):
        # Test adding an item successfully
        response = lambda_handler(self.test_events['add'], None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item 10 added successfully', response['body'])

    def test_remove_item(self):
        # Prepare by adding an item first
        lambda_handler(self.test_events['add'], None)

        # Test removing an item successfully
        response = lambda_handler(self.test_events['remove'], None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item 10 removed successfully', response['body'])

        # Test removing a non-existent item
        response = lambda_handler(self.test_events['remove'], None)
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Item 10 not found in the set', response['body'])

    def test_has_item(self):
        # Prepare by adding an item first
        lambda_handler(self.test_events['add'], None)

        # Test checking existence of an item that exists
        response = lambda_handler(self.test_events['has'], None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item 10 exists: True', response['body'])

        # Test checking existence of an item that does not exist
        lambda_handler(self.test_events['remove'], None)
        response = lambda_handler(self.test_events['has'], None)
        self.assertIn('Item 10 exists: False', response['body'])

    def test_bad_request(self):
        # Test handling of unsupported operation
        response = lambda_handler(self.test_events['bad_request'], None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Invalid operation specified', response['body'])

    def test_non_integer_item(self):
        # Test adding a non-integer item
        response = lambda_handler(self.test_events['non_int'], None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('The item must be an integer', response['body'])

if __name__ == '__main__':
    unittest.main()
