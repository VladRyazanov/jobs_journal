from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/4').json())
print(post('http://localhost:5000/api/v2/users', json={
    "email": "email",
    "surname": "surname",
    "name": "name",
    "age": 100,
    "position": "postion",
    "speciality": "speciality",
    "address": "address"
}).json())
print(delete('http://localhost:5000/api/v2/users/123').json())

