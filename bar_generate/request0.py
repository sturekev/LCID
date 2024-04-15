import requests
from PIL import Image
from io import BytesIO

""" send data (student id) to server
    receives and open a png of the barcode
"""


url = "http://127.0.0.1:8000/generate_barcode"
data = "389424723"

response = requests.get(f"{url}/{data}")

# print("content: ",response.content)
# print("bytesIO cont: ", BytesIO(response.content))
print(response)

if response.status_code == 200:
    try:
        # Attempt to open the image from the response content
        image_data = Image.open(BytesIO(response.content))

        # Display the image or perform additional processing as needed
        image_data.show()
    except Exception as e:
        print(f"Error opening image: {e}")
else:
    print(f"Error: {response.status_code} - {response.text}")

