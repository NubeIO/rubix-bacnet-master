import requests

host = '120.157.23.94'
port = '1618'
payload = {"username": "admin", "password": "N00BWires"}
get_token = requests.post(f"http://{host}:{port}/api/users/login", json=payload)
res = get_token.json()
access_token = res.get('access_token')

print(access_token)

# get_points = requests.get(url,
#                           headers={'Content-Type': 'application/json',
#                                    'Authorization': '{}'.format(access_token)})
# print(get_points.text)
port = '1616'
url = f'http://{host}:{port}/api/bacnet/points'

get_points = requests.get(url,
                          headers={'Content-Type': 'application/json'})
# print(get_points.text)
print(get_points.status_code)
_get_points = get_points.json()

for point in _get_points:
    uuid = point.get("uuid")
    object_name = point.get("object_name")
    url = f'http://{host}:{port}/api/bacnet/points/uuid/{uuid}'
    body = {
        "relinquish_default": 0
    }
    result = requests.patch(url,
                            headers={'Content-Type': 'application/json'},
                            json=body)
    print(result.status_code)
