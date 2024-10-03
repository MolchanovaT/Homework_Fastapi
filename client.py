import requests

# response = requests.post(
#     "http://127.0.0.1:8080/v1/user",
#     json={
#         "name": "user_1",
#         "password": "1234",
#         "is_admin": False,
#     },
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     "http://127.0.0.1:8080/v1/user",
#     json={
#         "name": "user_2",
#         "password": "5678",
#         "is_admin": False,
#     },
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     "http://127.0.0.1:8080/v1/user",
#     json={
#         "name": "admin",
#         "password": "1234",
#         "is_admin": True,
#     },
# )
# print(response.status_code)
# print(response.json())


response = requests.post(
    "http://127.0.0.1:8080/v1/login",
    json={
        "name": "admin",
        "password": "1234",
        "is_admin": True,
    },
)
print(response.status_code)
response_data = response.json()
print(response_data)
token = response_data["token"]

# response = requests.post(
#     "http://127.0.0.1:8080/v1/advertisement",
#     json={
#         "title": "Title",
#         "description": "descr",
#         "price": 100.00,
#     },
#     headers={"x-token": token},
# )
# print(response.status_code)
# print(response.json())

# response = requests.patch("http://127.0.0.1:8080/v1/advertisement/1", json={
#     "price": 300.00,
# }, headers={"x-token": token}, )
# print(response.status_code)
# print(response.json())

response = requests.delete("http://127.0.0.1:8080/v1/advertisement/1", headers={"x-token": token})
print(response.status_code)
print(response.json())
