from bitcoinlib.wallets import HDWallet, wallet_delete

from bitcoinlib.mnemonic import Mnemonic


passphrase = Mnemonic().generate()

print(passphrase)

wallet = HDWallet.create("mWallet1", keys=passphrase, network='bitcoin')

key1 = wallet.new_key()

print(key1.address)