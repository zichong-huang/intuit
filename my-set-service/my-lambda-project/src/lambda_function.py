import json

# Initialize the 'set_items' as a global variable
set_items = []

def lambda_handler(event, context):
    global set_items

    # Extract operation and item from query parameters for GET requests
    if event.get('httpMethod') == 'GET' or event.get('httpMethod') == 'DELETE':
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

    # Handle different operations based on the 'operation' value
    if operation == 'AddItem':
        if item not in set_items:
            set_items.append(item)
            return format_response(200, f'Item {item} added successfully. Current set: {set_items}')
        else:
            return format_response(200, f'Item {item} already exists in the set. No action taken.')

    elif operation == 'RemoveItem':
        if item in set_items:
            set_items.remove(item)
            return format_response(200, f'Item {item} removed successfully. Current set: {set_items}')
        else:
            return format_response(404, f'Item {item} not found in the set.')

    elif operation == 'HasItem':
        exists = item in set_items
        return format_response(200, f'Item {item} exists: {exists}.')

    elif operation == 'Reset':
        set_items = []
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
