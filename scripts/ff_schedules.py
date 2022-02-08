import json
import requests

host = 'rs-cba.nube-iiot.com'
port = '443'
payload = {"username": "admin", "password": "N00BWires"}
get_token = requests.post(f"https://{host}:{port}/api/users/login", json=payload)
res = get_token.json()
access_token = res.get('access_token')
print(access_token)

url = f'https://{host}:{port}/ff/api/flow_network_clones?with_stream_clones=true&with_consumers=true&with_tags=true&with_writers=true'

get_sch = requests.get(url,
                       headers={'Content-Type': 'application/json', 'Authorization': '{}'.format(access_token)},
                       json="")

new_holiday = {'59201e03-7356-4687-911f-c0840dad4977': {'color': '#d0021b', 'dates': [
    {'end': '2022-01-26T10:00:00.000Z', 'start': '2022-01-25T19:00:00.000Z'}], 'name': 'HVAC', 'value': 20}}  #austrlia day
count = 0
for streams in get_sch.json():
    print("=============================")
    stream_clones = streams.get("stream_clones")
    name = streams.get("name")
    site_id = streams.get("site_id")
    site_name = streams.get("site_name")
    device_name = streams.get("device_name")

    for consumers in stream_clones:
        consumers = consumers.get("consumers")
        # print(consumers)

        for writer in consumers:
            writer = writer.get("writers")
            for item in writer:
                writer_thing_class = item.get("writer_thing_class")
                if writer_thing_class == "schedule":
                    data_store = item.get("data_store")
                    holiday = data_store.get("holiday")
                    # update new holiday
                    data_store["holiday"] = new_holiday
                    # data_store["exceptions"] = new_holiday
                    if writer_thing_class == "schedule":
                        count += 1
                        print(count)
                        data_store = item.get("data_store")
                        uuid = item.get("uuid")
                        print("device_name", device_name, "name", name, "site_id", site_id, "site_name", site_name)
                        writer_url = f'https://{host}:{port}/ff/api/writers/action/{uuid}'
                        print(writer_url)
                        body = {
                            "action": "write",
                            "ask_refresh": True,
                            "schedule": {
                                "name": "HVAC",
                                "schedule": data_store
                            }
                        }
                        print(body)
                        if count <= 100:
                            new_sch = requests.post(writer_url,
                                                    headers={'Content-Type': 'application/json',
                                                             'Authorization': '{}'.format(access_token)},
                                                    json=body)
                            print(new_sch.status_code, "name", name)
                            if new_sch.status_code == 404:
                                print(new_sch.text)
                    # post new writer
