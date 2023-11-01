import requests

# Define the base URL of your FastAPI server
base_url = "http://127.0.0.1:8000"  # Replace with the actual URL of your FastAPI server

# Define the message you want to send
message = "convoi"

# Example using a GET request with a path parameter
response1 = requests.get(f"{base_url}/echo/{message}")

# Example using a POST request with a request body
data = {"message": message}
response2 = requests.post(f"{base_url}/receive_message/", json=data)

# Print the response from the server
print("response1")
print(response1.status_code)
print(response1.json())

print("response2")
print(response2.status_code)
print(response2.json())
