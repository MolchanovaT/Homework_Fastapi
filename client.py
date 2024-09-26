import requests

# response = requests.post(
#     "http://127.0.0.1:8080/v1/user",
#     json={
#         "name": "user1",
#     },
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     "http://127.0.0.1:8080/v1/advertisement",
#     json={
#         "title": "second ad",
#         "description": "description",
#         "price": 600.00,
#         "user_id": 1,
#     },
# )
# print(response.status_code)
# print(response.json())

# response = requests.patch("http://127.0.0.1:8080/v1/advertisement/2",
#                           json={
#                               "title": "new title",
#                               "price": 700.01,
#                           })
# print(response.status_code)
# print(response.json())

response = requests.delete("http://127.0.0.1:8080/v1/advertisement/2",)
print(response.status_code)
print(response.json())

