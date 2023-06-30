import json
import traceback
import requests
import re
import time

from threading import Thread, current_thread

from base_func import get_data, create_solana_request, get_block, get_current_block, get_data_no_timeout
from tg_bot import message, send_text_message
from price_table import get_table_prices
from unpack_metadata import get_metadata


def parse_trans(block_number):
    block_info = get_block(block_number)
    if block_info:
        try:
            for trans in block_info['transactions']:
                try:
                    if program_address in trans['meta']['logMessages'][0]\
                            and "Sell" in trans['meta']['logMessages'][1]:
                        nft_address = trans['meta']['preTokenBalances'][0]['mint']
                        metadata = get_metadata(nft_address)
                        nft_creator = str(metadata['data']['creators'][metadata['data']['verified'].index(1)], 'utf-8')
                        update_authority = str(metadata['update_authority'], 'utf-8')
                        nft_name = metadata['data']['name']
                        nft_symbol = metadata['data']['symbol']
                        nft_url = metadata['data']['uri']
                        for collection_update_authority in nft_prices.keys():
                            if collection_update_authority == update_authority:
                                if nft_prices[collection_update_authority][3] == nft_creator:
                                    for price_log in trans['meta']['logMessages']:
                                        if "price" in price_log:
                                            nft_price_from_log = re.search(r'\d{7,}', price_log)
                                            if nft_price_from_log:
                                                nft_price = float(nft_price_from_log[0]) / price_coeff
                                                if nft_price < nft_prices[collection_update_authority][1]:
                                                    nft_metadata = get_data_no_timeout(nft_url)
                                                    nft_level = int([key['value'] for key in nft_metadata['attributes'] if key['trait_type'] == 'Level'][0])
                                                    if nft_level == 3:
                                                        nft_link = f"https://magiceden.io/item-details/{nft_address}"
                                                        result_text = f"[{nft_prices[collection_update_authority][4][:-2]} level {nft_level}]({nft_link}) с ценой {nft_price}"
                                                        print(trans)
                                                        print(result_text)
                                                        send_text_message(message, result_text)
                                                break
                                    break
                except:
                    traceback.print_exc()
                    continue
        except KeyError:
            print(block_info)


def get_account_info(nft_address):
    params = [nft_address, {
        "encoding": "jsonParsed"
      }]
    return create_solana_request(params, "getAccountInfo")


def get_nft_name(nft_address):
    url = f"https://public-api.solscan.io/token/meta?tokenAddress={nft_address}"
    nft_name = get_data(url)
    if nft_name:
        if nft_name['name']:
            return nft_name['name']
        elif nft_name['symbol']:
            return nft_name['symbol']
    return False


def start_parser(parser_number):
    while True:
        try:
            block_number = get_current_block() - 1 - int(parser_number)
            print(block_number, parser_number)
            parse_trans(block_number)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    price_coeff = 1000000000
    prices_range = "A2:F31"
    percents_range = "M1:M2"
    program_address = ""
    solana_endpoint = "https://solana-api.projectserum.com"

    nft_prices = get_table_prices(prices_range, percents_range)
    print(nft_prices)

    # parse_trans(155615639)

    parser_1 = Thread(target=start_parser, args=('1'))
    parser_1.start()

    time.sleep(1)

    parser_2 = Thread(target=start_parser, args=('2'))
    parser_2.start()

    time.sleep(1)

    parser_3 = Thread(target=start_parser, args=('3'))
    parser_3.start()
