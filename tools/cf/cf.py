import os
import json
import requests

# internal
from tools.provider.provider import Cloudflare


# cfkv
def upload(config: Cloudflare, json_str: dict, key: str):
    # pip install requests
    email = config.CLOUDFLARE_EMAIL  # Cloudflare account email
    account_id = config.CLOUDFLARE_ACCOUNT_ID  # Cloudflare account ID
    namespace_id = config.CLOUDFLARE_KV_NAMESPACE_ID  # Cloudflare KV namespace ID
    api_key = config.CLOUDFLARE_API_KEY  # Cloudflare API key

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk"

    data = [{"key": key, "value": json_str}]

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"\033[31mdata {key[:6]} have uploaded to cloudflare kv \033[0m")
    else:
        print("error:", response.status_code, response.text)

import requests

def get(config: Cloudflare, key: str)->dict:
    email = config.CLOUDFLARE_EMAIL  # Cloudflare account email
    account_id = config.CLOUDFLARE_ACCOUNT_ID  # Cloudflare account ID
    namespace_id = config.CLOUDFLARE_KV_NAMESPACE_ID  # Cloudflare KV namespace ID
    api_key = config.CLOUDFLARE_API_KEY  # Cloudflare API key

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}"

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"\033[31mError: {response.status_code}, {response.text}\033[0m")  # 红色错误信息
        return {}

