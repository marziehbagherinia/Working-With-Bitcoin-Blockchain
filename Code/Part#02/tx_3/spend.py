import bitcoin.wallet
from bitcoin.core import Hash160, key
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_EQUAL
from bitcoinaddress import Key
from utils import create_OP_CHECKSIG_signature, create_txout, create_txin, create_signed_transaction, broadcast_transaction

bitcoin.SelectParams("testnet") #Select the network (testnet or mainnet)

my_key = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqcieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key = bitcoin.wallet.CBitcoinSecret(my_key.testnet.wif)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

dest_key = Key.of('5JbTZ4zCTn1rwCfdkPWLbdFgqzieGaG9Qjp3iRhf7R8gNroj4KM')
dest_private_key = bitcoin.wallet.CBitcoinSecret(dest_key.testnet.wif)
dest_public_key = dest_private_key.pub
dest_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(dest_public_key)

txin_redeemScript = CScript([my_public_key, OP_CHECKSIG])

def P2PKH_scriptPubKey_out(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptPubKey(address):
    redeemScript = CScript([address, OP_CHECKSIG])
    return [OP_HASH160, bitcoin.core.Hash160(redeemScript), OP_EQUAL]

def P2PKH_scriptSig(txin, txout):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_redeemScript, my_private_key)
    return [signature, txin_redeemScript] #Fill this section

def send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey):
    
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    print(my_address)
    print(my_public_key.hex())
    print(my_private_key.hex())

    txid_to_spend = ('5bf6358f7b3077c65eefa205623cfa66d94f4cc9417e18d563b18c77e0939440') #Hash tx k faucet BTC dade
    utxo_index = 0 # UTXO index among transaction outputs

    #Outputs
    amount_to_send = 0.0128
    txout_scriptPubKey = P2PKH_scriptPubKey_out(dest_public_key)
    
    response = send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result