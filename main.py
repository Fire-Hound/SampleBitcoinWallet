from bit import PrivateKeyTestnet
import bit

def create_wallet():
    my_key = PrivateKeyTestnet(wif="cSDtqh8zGxiZjQGL2TmSbqnBSDDQ1fsJWDiGPP7L8eRZDHe4ycJd")
    print(my_key.version)
    print(my_key.to_wif())
    print(my_key.address)
    print(my_key.get_balance(currency="mbtc"))
    print(my_key.get_transactions())
    return {"wallet_id":my_key.to_wif(), "address":my_key.address}

def get_wallet(wallet_id):
    return PrivateKeyTestnet(wif=wallet_id)

print(create_wallet()["address"])
# tx_hash = my_key.send([('mkH41dfD4S8DEoSfcVSvEfpyZ9siogWWtr', 1, 'satoshi')])
# print(tx_hash)
