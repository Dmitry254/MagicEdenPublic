import requests
import json


solana_endpoint = "https://solana-api.projectserum.com"


def get_data(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        req = requests.get(url, headers, timeout=3.1)
        if req:
            res = json.loads(req.text)
        else:
            res = {}
    except requests.exceptions.ConnectTimeout:
        res = {}
    except requests.exceptions.ReadTimeout:
        res = {}
    return res


def get_data_no_timeout(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        req = requests.get(url, headers)
        if req:
            res = json.loads(req.text)
        else:
            res = {}
    except requests.exceptions.ConnectTimeout:
        res = {}
    except requests.exceptions.ReadTimeout:
        res = {}
    return res


def post_data_no_timeout(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        req = requests.post(url, headers)
        if req:
            res = json.loads(req.text)
        else:
            res = {}
    except requests.exceptions.ConnectTimeout:
        res = {}
    except requests.exceptions.ReadTimeout:
        res = {}
    return res


def create_solana_request(params, method):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(solana_endpoint, headers=headers, data=payload).json()
    if "result" in response.keys():
        return response['result']
    return response


def get_current_block():
    params = []
    return create_solana_request(params, "getSlot")


def get_block(block_number):
    params = [block_number, {"encoding": "json", "transactionDetails": "full", "rewards": False}]
    block_info = create_solana_request(params, "getBlock")
    if "error" in block_info.keys():
        if block_info['error']['code'] == -32007 or block_info['error']['code'] == -32004:
            return {}
    return block_info
