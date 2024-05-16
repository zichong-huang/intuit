import json
import logging

# Initialize the 'set_items' as a global variable
set_items = []

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    global set_items
    logger.info(f"Event: {json.dumps(event)}")

    # Extract HTTP method
    http_method = event.get('httpMethod')

    # Extract operation and item from query parameters for GET and DELETE requests
    if http_method == 'GET' or http_method == 'DELETE':
        operation = event.get('queryStringParameters', {}).get('operation')
        item = event.get('queryStringParameters', {}).get('item')
    else:
        # Handle other HTTP methods that include a body
        body = event.get("body", "{}")
        if body:
            body = json.loads(body)
        else:
            body = {}

        operation = body.get('operation')
        item = body.get('item')

    # Try to convert item to integer, handle possible ValueError
    if item is not None:
        try:
            item = int(item)
        except (TypeError, ValueError):
            return format_response(400, 'The item must be an integer.')

    # Handle different operations based on the 'operation' value or HTTP method
    if operation == 'AddItem' or (http_method == 'POST' and operation is None):
        if item not in set_items:
            set_items.append(item)
            return format_response(200, f'Item {item} added successfully. Current set: {set_items}')
        else:
            return format_response(200, f'Item {item} already exists in the set. No action taken.')

    elif operation == 'RemoveItem' or (http_method == 'DELETE' and operation is None):
        if item in set_items:
            set_items.remove(item)
            return format_response(200, f'Item {item} removed successfully. Current set: {set_items}')
        else:
            return format_response(404, f'Item {item} not found in the set.')

    elif operation == 'HasItem' or (http_method == 'GET' and operation is None):
        exists = item in set_items
        return format_response(200, f'Item {item} exists: {exists}.')

    elif operation == 'Reset' or (http_method == 'POST' and operation == 'Reset'):
        set_items.clear()
        return format_response(200, 'Set items have been reset.')

    else:
        return format_response(400, 'Invalid operation specified. Available operations are AddItem, RemoveItem, HasItem, and Reset.')

def format_response(status_code, message):
    """
    Helper function to format the JSON response in a way that API Gateway expects.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": message})
    }
