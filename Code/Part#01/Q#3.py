import hashlib
import ecdsa
import binascii
from bitcoinaddress import Key

PREFIX_EVEN = b'\x02'
PREFIX_ODD = b'\x03'
WITNESS_VERSION = 0x00
BECH32_PREFIX = "tb"

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def ripemd(v):
    r = hashlib.new('ripemd160')
    r.update(v)
    return r

def sha256(v):
    return hashlib.sha256(v)

def hash160(v):
    return ripemd(hashlib.sha256(v).digest())

def ecdsa_secp256k1(digest):
    sk = ecdsa.SigningKey.from_string(digest, curve=ecdsa.SECP256k1)
    return sk.get_verifying_key()

def bech32_polymod(values):
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk

def bech32_hrp_expand(hrp):
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    """Compute a Bech32 string given HRP and data values."""
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def convertbits(data, frombits, tobits, pad=True):
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def encode(hrp, witver, witprog):
    """Encode a segwit address."""
    ret = bech32_encode(hrp, [witver] + convertbits(witprog, 8, 5))
    return ret

def get_pubkey(key):
    ecdsa_digest = ecdsa_secp256k1(key.digest).to_string()
    x_coord = ecdsa_digest[:int(len(ecdsa_digest) / 2)]
    y_coord = ecdsa_digest[int(len(ecdsa_digest) / 2):]
    if int(binascii.hexlify(y_coord), 16) % 2 == 0:
        p = PREFIX_EVEN + x_coord
    else:
        p = PREFIX_ODD + x_coord
    
    pubkeyc = str(binascii.hexlify(p).decode('utf-8'))
    return p, pubkeyc

def get_bech32(key):
    p, pubkeyc = get_pubkey(key)
    redeem_script_P2WPKH = hash160(p).digest()  # 20 bytes
    return str(encode(BECH32_PREFIX, WITNESS_VERSION, redeem_script_P2WPKH)), pubkeyc

if __name__ == '__main__':
    private_key = Key.of('5JbTZ4zCTn1rwCfdkPWLddFgqzieGaG9Qjp3iRhf7R8gNroj4KM')
    segwit_address, public_key = get_bech32(private_key)
    print("Private key in WIF format is:", private_key.testnet.wif)
    print("Public key is:", public_key)
    print("Segwit address is:", segwit_address)