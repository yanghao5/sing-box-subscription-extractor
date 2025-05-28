import os
from typing import List

# internal pkg
from core.provider.provider import Providers

# third-party pkg
import requests

def download_subscribe(subscribe_url: str, file_path: str):
    url = subscribe_url

    # User-Agent
    headers = {"User-Agent": "sing-box"}

    # Get
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("\033[34m The original subscription was successfully downloaded and saved as " + "\033[33m"+file_path + " \033[0m\n")

    else:
        print(f"\033[34m Download failed, status code: {response.status_code}\n")


def fetcher(p: Providers) -> List:
    rawdata_list = []
    os.makedirs("temp/raw", exist_ok=True)
    for sub in p.subscribe:
        print(f"\033[34m URL: \033[33m{sub.url}\033[34m, Tag: \033[33m{sub.tag} \033[0m\n")
        file_path = os.path.join("temp/raw", sub.tag + ".json")
        download_subscribe(sub.url, file_path)
        rawdata_list.append(file_path)
    return rawdata_list