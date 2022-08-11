import time
import datetime
from hashlib import sha256
from bitcoinaddress import Key
import bitcoin.wallet
from bitcoin.core import Hash160, b2x
from bitcoin.core.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
from utils_spend import create_txout, create_txin, create_signed_transaction

bitcoin.SelectParams("testnet") #Select the network (testnet or mainnet)

DIFFICAULTY = 8
MAX_NONCE = 4294967295 #0xffffffff

my_key = Key.of('5JbTZ4zCTn1qwCfdkPWLbdFgqzieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key = bitcoin.wallet.CBitcoinSecret(my_key.testnet.wif)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey_out(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptPubKey(address):
    return []

def P2PKH_scriptSig():
    return [Hash160(b"3831303139373638324d61727a696568426167686572696e6961416d697269")] #Hash(810197682MarziehBagheriniaAmiri)

def send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send_1, txout_scriptPubKey_1):
    
    txout_1 = create_txout(amount_to_send_1, txout_scriptPubKey_1)
    
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig()

    new_tx = create_signed_transaction(txin, txout_1, txin_scriptPubKey, txin_scriptSig)

    return b2x(new_tx.serialize())

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(transactions, previous_hash, prefix_zeros):
    prefix_str = '0' * prefix_zeros

    for nonce in range(16777215, MAX_NONCE):
        text = transactions + previous_hash + str(hex(nonce)[2:])
        new_hash = SHA256(SHA256(text))
        if new_hash.startswith(prefix_str):
            return nonce, new_hash

    raise BaseException(f"Couldn't solve block after trying {MAX_NONCE} times")

if __name__ == '__main__':

    txid_to_spend = ('0000000000000000000000000000000000000000000000000000000000000000')
    utxo_index = 0xffffffff

    amount_to_send = 6.25
    txout_scriptPubKey = P2PKH_scriptPubKey_out(my_public_key)

    coinbase_tx = send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey)

    start = time.time()
    print("start mining")
    Nonce, new_hash = mine(coinbase_tx,'00000000063a3773c9ac36ff6bae5e78bccaf453796474250f41dad40c1c6c45', DIFFICAULTY)
    total_time = str((time.time() - start))
    print(f"end mining. Mining took: {total_time} seconds")
    
    print()
    print("Hash:", new_hash)
    print("Timestamp:", datetime.datetime.now())
    print("Miner:", "MBA")
    print("Number of Transactions:", 1)
    print("Difficulty:", DIFFICAULTY)
    print("Merkle root:", SHA256(coinbase_tx))
    print("Nonce:", Nonce)
    print("Block Reward:", 6.25, "BTC")
    print("Fee Reward:", 0, "BTC")