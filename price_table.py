import requests
import json

from datetime import datetime

from base_func import get_data
from google_sheets import get_google_sheet_data


def get_table_prices(prices_range, percents_range):
    nft_prices = {}
    percents_list = get_google_sheet_data(percents_range)
    profit = float(percents_list[0][0].replace(',', '.'))
    taxes = float(percents_list[1][0].replace(',', '.'))
    nft_list = get_google_sheet_data(prices_range)
    for nft in nft_list:
        nft_name = nft[0]
        nft_symbol = nft[1]
        nft_creator = nft[2]
        update_authority = nft[3]
        nft_sell_price = float(nft[4].replace(',', '.'))
        royalty = float(nft[5].replace(',', '.'))
        nft_buy_price = nft_sell_price / (1 + royalty + profit + taxes)
        nft_prices.update({update_authority: [nft_sell_price, nft_buy_price, nft_symbol, nft_creator, nft_name]})
    return nft_prices


if __name__ == "__main__":
    print(get_table_prices())
