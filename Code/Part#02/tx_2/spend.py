import bitcoin.wallet
from bitcoin.core import Hash160, key
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_EQUAL, OP_2, OP_3, OP_CHECKMULTISIG, OP_0
from bitcoinaddress import Key
from utils import create_OP_CHECKSIG_signature, create_txout, create_txin, create_signed_transaction, broadcast_transaction

bitcoin.SelectParams("testnet") #Select the network (testnet or mainnet)

my_key_1 = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqcieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key_1 = bitcoin.wallet.CBitcoinSecret(my_key_1.testnet.wif)
my_public_key_1 = my_private_key_1.pub
my_address_1 = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key_1)

my_key_2 = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqcieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key_2 = bitcoin.wallet.CBitcoinSecret(my_key_2.testnet.wif)
my_public_key_2 = my_private_key_2.pub
my_address_2 = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key_2)

my_key_3 = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqcieGaG9Qjp3iRhf7R8gNroj4KM')
my_private_key_3 = bitcoin.wallet.CBitcoinSecret(my_key_3.testnet.wif)
my_public_key_3 = my_private_key_3.pub
my_address_3 = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key_3)

dest_key = Key.of('5JbTZ4zCTn1qwCfdkPWLbdFgqzieGaG9Qjp3iRhf7R8gNroj4KM')
dest_private_key = bitcoin.wallet.CBitcoinSecret(dest_key.testnet.wif)
dest_public_key = dest_private_key.pub
dest_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(dest_public_key)

def P2PKH_scriptPubKey_out(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptPubKey():
    return [OP_2, my_public_key_1, my_public_key_2, my_public_key_3, OP_3, OP_CHECKMULTISIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature_1 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key_1)
    signature_2 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key_2)
    return [OP_0, signature_1, signature_2] #Fill this section

def send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey):
    
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':

    txid_to_spend = ('c0947841f5babc8a692db269c907db8a03709b327a128f483da974bb889f9513') #Hash tx k faucet BTC dade
    utxo_index = 0 # UTXO index among transaction outputs

    #Outputs
    amount_to_send = 0.01745
    txout_scriptPubKey = P2PKH_scriptPubKey_out(dest_public_key)
    
    response = send_from_P2PKH_transaction(txid_to_spend, utxo_index, amount_to_send, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result