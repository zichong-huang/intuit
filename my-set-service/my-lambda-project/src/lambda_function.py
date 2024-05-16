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
    item = None
    operation = None

    # Extract item from query parameters for GET and DELETE requests
    if http_method in ['GET', 'DELETE']:
        if 'queryStringParameters' in event:
            item = event.get('queryStringParameters', {}).get('item')
        else:
            logger.error("Query string parameters missing in GET/DELETE request")
            return format_response(400, 'Query string parameters are required for GET and DELETE requests.')
    else:
        # Handle other HTTP methods that include a body
        body = event.get("body", "{}")
        if body:
            body = json.loads(body)
        else:
            body = {}

        item = body.get('item')
        operation = body.get('operation')

    # Log extracted parameters
    logger.info(f"HTTP Method: {http_method}, Item: {item}, Operation: {operation if http_method == 'POST' else 'N/A'}")

    # Try to convert item to integer, handle possible ValueError
    if item is not None:
        try:
            item = int(item)
        except (TypeError, ValueError):
            logger.error("The item must be an integer.")
            return format_response(400, 'The item must be an integer.')

    # Handle different operations based on the HTTP method
    if http_method == 'POST':
        if operation == 'AddItem':
            if item not in set_items:
                set_items.append(item)
                return format_response(200, f'Item {item} added successfully. Current set: {set_items}')
            else:
                return format_response(200, f'Item {item} already exists in the set. No action taken.')
        elif operation == 'Reset':
            set_items.clear()
            return format_response(200, 'Set items have been reset.')
        else:
            logger.error("Invalid operation specified in POST request.")
            return format_response(400, 'Invalid operation specified. Available operations are AddItem, RemoveItem, HasItem, and Reset.')

    elif http_method == 'DELETE':
        if item in set_items:
            set_items.remove(item)
            return format_response(200, f'Item {item} removed successfully. Current set: {set_items}')
        else:
            return format_response(404, f'Item {item} not found in the set.')

    elif http_method == 'GET':
        exists = item in set_items
        return format_response(200, f'Item {item} exists: {exists}.')

    else:
        logger.error("Unsupported HTTP method.")
        return format_response(400, 'Unsupported HTTP method.')

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
