def get_collections_info():
    for collection_name in collections_list.keys():
        print(collection_name)
        collection_activity = get_collection_activity(collection_name)
        print(collection_activity)


def get_collection_activity(collection_name):
    url = f"https://api-devnet.magiceden.dev/v2/collections/{collection_name}/activities?offset=0&limit=100"
    collection_activity = get_data(url)
    return collection_activity


def get_collection_metrics(collection_name):
    url = f"https://api-mainnet.magiceden.io/rpc/getAggregatedCollectionMetricsBySymbol?edge_cache=true&symbols={collection_name}"
    collection_metrics = get_data(url)
    return collection_metrics


def get_popular_collections():
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    print(date)
    url = f"https://api-mainnet.magiceden.io/popular_collections?more=true&timeRange=7d&edge_cache=true"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "access-control-allow-credentials": "true",
        "access-control-allow-origin": "https://magiceden.io",
        "alt-svc": 'h3=":443"; ma=86400, h3-29=":443"; ma=86400',
        "cache-control": "public, max-age = 600, s-maxage = 600",
        "cdn-cache-control": "public, max-age=600, s-maxage=600",
        "cf-cache-status": "REVALIDATED",
        "cf-ray": "7300fa2ddf603a55-DME",
        "content-encoding": "br",
        "content-type": "application/json; charset=utf-8",
        "date": date,
        "etag": 'W/"10286-6wagn1sD8okvNaC2nAaF8vCF35g"',
        "expect-ct": 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
        "server": "cloudflare",
        "vary": "Origin, Accept-Encoding",
        "x-ratelimit-limit": "120",
        "x-ratelimit-remaining": "115",
        "x-ratelimit-reset": "1658706304",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',

    }
    popular_collections = requests.get(url, headers=headers)
    return popular_collections