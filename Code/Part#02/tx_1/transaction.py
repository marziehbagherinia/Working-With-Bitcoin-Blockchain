import bitcoin.wallet
from bitcoin.core import Hash160
from bitcoin.core.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_RETURN
from bitcoinaddress import Key
from utils import create_OP_CHECKSIG_signature, create_txout, create_txin, create_signed_transaction, broadcast_transaction

bitcoin.SelectParams("testnet") #Select the network (testnet or mainnet)

my_key = Key.of('5JbTZ4zCTn1rzCfdkPWLbdFgqzieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key = bitcoin.wallet.CBitcoinSecret(my_key.testnet.wif)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
#destination_address = bitcoin.wallet.CBitcoinAddress('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') # Destination address (recipient of the money)

def P2PKH_scriptPubKey_1(address):
    return [OP_RETURN, Hash160(address)]

def P2PKH_scriptPubKey_2(address):
    return []

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout_1, txout_2, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout_1, txout_2, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key] #Fill this section

def send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send_1, txout_scriptPubKey_1, amount_to_send_2, txout_scriptPubKey_2):
    
    txout_1 = create_txout(amount_to_send_1, txout_scriptPubKey_1)
    txout_2 = create_txout(amount_to_send_2, txout_scriptPubKey_2)
    
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout_1, txout_2, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout_1, txout_2, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    print(my_address)
    print(my_public_key.hex())
    print(my_private_key.hex())

    txid_to_spend = ('4b4591fb05155e5ec9d1d3965184ad4ae2922182f931fa784c5b682db950fb95')
    utxo_index = 0

    #Outputs
    #No one can spend
    amount_to_send_1 = 0.0
    txout_scriptPubKey_1 = P2PKH_scriptPubKey_1(my_address)
    
    #Everyone can spend.
    amount_to_send_2 = 0.0155
    txout_scriptPubKey_2 = P2PKH_scriptPubKey_2(my_address)
    
    response = send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send_1, txout_scriptPubKey_1, amount_to_send_2, txout_scriptPubKey_2)
    print(response.status_code, response.reason)
    print(response.text)