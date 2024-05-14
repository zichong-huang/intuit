import requests

def make_request(method, url, operation, item):
    """ General helper function for making HTTP requests. """
    headers = {'Content-Type': 'application/json'}
    # Prepare the correct parameters based on the request method
    params = {"operation": operation, "item": str(item)} if method == 'GET' else None
    data = {"operation": operation, "item": str(item)} if method in ["POST", "DELETE"] else None

    # Adjust request handling based on the method
    if method in ["POST", "DELETE"]:
        response = requests.request(method, url, json=data, headers=headers)
    elif method == "GET":
        response = requests.get(url, params=params, headers=headers)

    # Process and print the response
    if response.ok:
        try:
            response_data = response.json()
            print(f"{operation} {item}: {response_data}")
        except ValueError:
            print(f"Failed to decode JSON from response: {response.text}")
    else:
        print(f"Error {response.status_code} during {operation}: {response.text}")

    return response

base_url = "https://a541wh2ca6.execute-api.us-east-1.amazonaws.com/prod/"

def test_operations():
    items = [10, 20, 30]

    # Adding items
    print("Adding Items:")
    for item in items:
        make_request('POST', f"{base_url}addItem", "AddItem", item)

    # Removing one item
    print("\nRemoving Item:")
    make_request('DELETE', f"{base_url}removeItem", "RemoveItem", 20)

    # Checking remaining items
    print("\nChecking Remaining Items:")
    for item in items:
        make_request('GET', f"{base_url}hasItem", "HasItem", item)

if __name__ == "__main__":
    test_operations()
