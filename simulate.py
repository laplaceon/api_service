import requests
import random
import time

url = "http://localhost:5000"  # Your API URL

# List of good and bad requests
good_requests = [
    {"url": "/charge", "method": "post", "data": {"orderid": "123"}},
    {"url": "/charge", "method": "post", "data": {"orderid": "456"}},
    {"url": "/charge", "method": "post", "data": {"orderid": "789"}},
    {"url": "/charge", "method": "post", "data": {"orderid": "135"}},
    {"url": "/slow-query", "method": "post", "data": {"query": "SELECT * FROM customers"}},
    {"url": "/slow-query", "method": "post", "data": {"query": "SELECT * FROM products"}},
    # {"url": "/invalid-login", "method": "post", "data": {"username": "johndoe", "password": "password123"}},
    # {"url": "/invalid-login", "method": "post", "data": {"username": "janedoe", "password": "password456"}},
    {"url": "/", "method": "get"},
    {"url": "/status", "method": "get"}
]

# bad_requests = [
#     {"url": "/charge", "method": "post", "data": {"orderid": "555"}},
#     {"url": "/charge", "method": "post", "data": {"orderid": "322"}},
#     {"url": "/slow-query", "method": "post", "data": {"query": "SELECT * FROM large_table JOIN other_large_table"}},
#     {"url": "/slow-query", "method": "post", "data": {"query": "SELECT * FROM huge_table"}},
#     {"url": "/invalid-login", "method": "post", "data": {"username": "fakeuser", "password": "badpass"}},
#     {"url": "/invalid-login", "method": "post", "data": {"username": "baduser", "password": "wrongpw"}},
#     {"url": "/", "method": "get"},
#     {"url": "/foo", "method": "get"}
# ]

bad_requests = [
    {"url": "/charge", "method": "post", "data": {"orderid": "555"}, "expected_status": 500},
    {"url": "/charge", "method": "post", "data": {"orderid": "322"}, "expected_status": 500},
    {"url": "/slow-query", "method": "post", "data": {"query": "SELECT * FROM large_table JOIN other_large_table"}, "expected_status": 400}
]

num_requests = 100 # Total number of requests
bad_indices = [50, 100, 150]  # Indices at which to send bad requests
bad_counter = 0  # Counter to track which bad request to send

for i in range(num_requests):
    # Pick a good request by default
    request_data = random.choice(good_requests)

    # If the current index is in bad_indices, pick the corresponding bad request
    if i in bad_indices:
        request_data = random.choice(bad_requests)
    # Send the request
    if request_data["method"] == "post":
        response = requests.post(url + request_data["url"], json=request_data["data"])
    elif request_data["method"] == "get":
        response = requests.get(url + request_data["url"])
    
    print(f"Sent request to {request_data['url']}, got status code {response.status_code}")

    # Wait for a random amount of time between 0.1 and 0.5 seconds
    time.sleep(random.uniform(0.1, 0.5))