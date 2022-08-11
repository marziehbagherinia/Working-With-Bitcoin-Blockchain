import os
import hashlib

testnet_public_prefix = b"\x6F"
testnet_private_prefix = b"\xEF"

gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1

class secp256k1:
    def __init__(self, x = gx, y = gy, p = p):
        self.x = x
        self.y = y
        self.p = p

    def __add__(self, other):
        return self.__radd__(other)

    def __mul__(self, other):
        return self.__rmul__(other)

    def __rmul__(self, other):
        n = self
        q = None

        for i in range(256):
            if other & (1 << i):
                q = q + n
            n = n + n

        return q

    def __radd__(self, other):
        if other is None:
            return self
        x1 = other.x
        y1 = other.y
        x2 = self.x
        y2 = self.y
        p = self.p

        if self == other:
            l = pow(2 * y2 % p, p-2, p) * (3 * x2 * x2) % p
        else:
            l = pow(x1 - x2, p-2, p) * (y1 - y2) % p

        newX = (l ** 2 - x2 - x1) % p
        newY = (l * x2 - l * newX - y2) % p

        return secp256k1(newX, newY)

    def toBytes(self):
        x = self.x.to_bytes(32, "big")
        y = self.y.to_bytes(32, "big")
        return b"\x04" + x + y



def sha256(data):
    digest = hashlib.new("sha256")
    digest.update(data)
    return digest.digest()


def ripemd160(x):
    d = hashlib.new("ripemd160")
    d.update(x)
    return d.digest()


def base_58(data):
    b58_str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    result = ""

    if data[0] == 0:
        return "1" + base_58(data[1:])

    x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
    
    while x > 0:
        result = b58_str[x % 58] + result
        x = x // 58

    return result

def getWif(private_key):
    wif = testnet_private_prefix + private_key
    wif = base_58(wif + sha256(sha256(wif))[:4])
    return wif

def get_address(private_key):
    SPEC256k1 = secp256k1()
    k = int.from_bytes(private_key, "big")
    public_key = ripemd160(sha256((SPEC256k1 * k).toBytes()))
    address = testnet_public_prefix + public_key
    base58_address = base_58(address + sha256(sha256(address))[:4])
    return base58_address

private_key = os.urandom(32)
wif_private_key = getWif(private_key)
base58_address = get_address(private_key)

print("Private key in WIF format is: ", wif_private_key)
print("Address in Base58 format is: ", base58_address)