import requests
from time import sleep
if __name__ == "__main__":
    host = 'localhost'
    payload = {"username": "admin", "password": "N00BWires"}
    get_token = requests.post(f"http://{host}:1616/api/users/login", json=payload)
    res = get_token.json()
    token = res.get('access_token')
    print(token)
    payload = [{"service": "RUBIX_PLAT", "version": "latest"}]
    # access_token = token
    url = f"http://{host}:1616/api/app/download"
    download_state_url = f"http://{host}:1616/api/app/download_state"
    result = requests.post(url,
                           headers={'Content-Type': 'application/json'},
                           json=payload)
    if result.status_code != 200:
        print("Failed to download", result.json())
        print("Clearing download state...")
        requests.delete(download_state_url,
                        headers={'Content-Type': 'application/json'},
                        json=payload)
        print("Download state is cleared...")
    else:
        print("Download process has been started, and waiting for it's completion...")
        while True:
            sleep(1)
            download_state = requests.get(download_state_url,
                                          headers={'Content-Type': 'application/json'},
                                          json=payload)
            print('download_state', download_state.json())
            if download_state.json().get('state') == 'DOWNLOADED':
                break
        print("Download completed...")
        print("Starting installation...")
        result = requests.post(f"http://{host}:1616/api/app/install",
                               headers={'Content-Type': 'application/json'},
                               json=payload)
        print("Installation completed....", result.json())
        print("Clearing download state...")
        requests.delete(download_state_url,
                        headers={'Content-Type': 'application/json'},
                        json=payload)
        print("Download state is cleared...")