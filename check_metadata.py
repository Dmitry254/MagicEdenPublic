import json
import traceback
import requests
import re
import time

from threading import Thread, current_thread

from base_func import get_data, create_solana_request, get_block, get_current_block
from price_table import get_table_prices
from unpack_metadata import get_metadata


def parse_trans(block_numbers):
    for block_number in block_numbers:
        block_info = get_block(block_number)
        if block_info:
            try:
                for trans in block_info['transactions']:
                    try:
                        if program_address in trans['meta']['logMessages'][0] \
                                and "Sell" in trans['meta']['logMessages'][1]:
                            nft_address = trans['meta']['preTokenBalances'][0]['mint']
                            metadata = get_metadata(nft_address)
                            nft_creator = str(metadata['data']['creators'][metadata['data']['verified'].index(1)],
                                              'utf-8')
                            update_authority = str(metadata['update_authority'], 'utf-8')
                            nft_name = metadata['data']['name']
                            nft_symbol = metadata['data']['symbol']
                            for collection_update_authority in nft_prices.keys():
                                if collection_update_authority == update_authority:
                                    if nft_prices[collection_update_authority][3] == nft_creator:
                                        for price_log in trans['meta']['logMessages']:
                                            if "price" in price_log:
                                                nft_price_from_log = re.search(r'\d{7,}', price_log)
                                                if nft_price_from_log:
                                                    nft_price = float(nft_price_from_log[0]) / price_coeff
                                                    nft_link = f"https://magiceden.io/item-details/{nft_address}"
                                                    result_text = f"[{nft_prices[collection_update_authority][4][:-2]}]({nft_link}) с ценой {nft_price}"
                                                    print(trans)
                                                    print(result_text)
                                                    break
                                        break
                    except:
                        traceback.print_exc()
            except KeyError:
                print(block_info)


if __name__ == "__main__":
    price_coeff = 1000000000
    prices_range = "A2:F31"
    percents_range = "M1:M2"
    program_address = ""
    solana_endpoint = "https://solana-api.projectserum.com"

    block_numbers = []

    nft_prices = get_table_prices(prices_range, percents_range)
    print(nft_prices)

    parse_trans(block_numbers)
