import bitcoin.wallet
from bitcoin.core import Hash160, key
from bitcoin.core.script import CScript, OP_0, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_EQUAL
from bitcoinaddress import Key
from utils import create_OP_CHECKSIG_signature, create_txout, create_txin, create_signed_transaction, broadcast_transaction

bitcoin.SelectParams("testnet") #Select the network (testnet or mainnet)

my_key = Key.of('5JbTZ4zCTn1rwCfdkPWLbdFgqzieGaG9Qjp3iRhg7R8gNroj4KM')
my_private_key = bitcoin.wallet.CBitcoinSecret(my_key.testnet.wif)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

dest_key = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqcieGaG9Qjp3iRhf7R8gNroj4KM')
dest_private_key = bitcoin.wallet.CBitcoinSecret(dest_key.testnet.wif)
dest_public_key = dest_private_key.pub
dest_scriptPubKey = CScript([OP_0, Hash160(dest_public_key)])
dest_address = bitcoin.wallet.P2WPKHBitcoinAddress.from_scriptPubKey(dest_scriptPubKey)
#dest_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(dest_public_key)

def P2PKH_scriptPubKey_out(address):
    return [OP_0, Hash160(address)]

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key] #Fill this section

def send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey):
    
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    print(my_address)
    print(my_public_key.hex())
    print(my_private_key.hex())

    txid_to_spend = ('267288b025296e28517d0c7b413461e76837aac6ad484143ee02232a9d06788f') #Hash tx k faucet BTC dade
    utxo_index = 1 # UTXO index among transaction outputs

    #Outputs
    amount_to_send = 0.0331
    txout_scriptPubKey = P2PKH_scriptPubKey_out(dest_public_key)
    
    response = send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result