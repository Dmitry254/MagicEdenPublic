import base58
import base64
import struct

from solana.publickey import PublicKey

from base_func import create_solana_request

METADATA_PROGRAM_ID = PublicKey('')
SYSTEM_PROGRAM_ID = PublicKey('')
SYSVAR_RENT_PUBKEY = PublicKey('')
ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID = PublicKey('')
TOKEN_PROGRAM_ID = PublicKey('')


def get_account_info(nft_address):
    params = [nft_address, {
        "encoding": "jsonParsed"
      }]
    return create_solana_request(params, "getAccountInfo")


def get_metadata(nft_address):
    metadata_account = str(get_metadata_account(nft_address))
    data = base64.b64decode(get_account_info(metadata_account)['value']['data'][0])
    metadata = unpack_metadata(data)
    return metadata


def unpack_metadata(data):
    assert (data[0] == 4)
    i = 1
    source_account = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
    i += 32
    mint_account = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
    i += 32
    name_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    name = struct.unpack('<' + "B" * name_len, data[i:i + name_len])
    i += name_len
    symbol_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    symbol = struct.unpack('<' + "B" * symbol_len, data[i:i + symbol_len])
    i += symbol_len
    uri_len = struct.unpack('<I', data[i:i + 4])[0]
    i += 4
    uri = struct.unpack('<' + "B" * uri_len, data[i:i + uri_len])
    i += uri_len
    fee = struct.unpack('<h', data[i:i + 2])[0]
    i += 2
    has_creator = data[i]
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack('<I', data[i:i + 4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(bytes(struct.unpack('<' + "B" * 32, data[i:i + 32])))
            creators.append(creator)
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    metadata = {
        "update_authority": source_account,
        "mint": mint_account,
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata


def get_metadata_account(mint_key):
    return PublicKey.find_program_address(
        [b'metadata', bytes(METADATA_PROGRAM_ID), bytes(PublicKey(mint_key))],
        METADATA_PROGRAM_ID
    )[0]


if __name__ == "__main__":
    metadata = get_metadata("")
    print(metadata)
    metadata = get_metadata("")
    print(metadata)
