import requests

url = "http://localhost:5000/images/upload"
file_path = "../data/test_image.jpg"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": ("test_image.jpg", file, "image/jpeg")})

print(f"🔍 Status Code: {response.status_code}")
print(f"🔍 Response Body: {response.text}")
