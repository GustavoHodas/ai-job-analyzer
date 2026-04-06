import requests

def fetch_jobs():
    url = "https://arbeitnow.com/api/job-board-api"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        return None