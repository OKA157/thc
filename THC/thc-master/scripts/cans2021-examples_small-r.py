from thc.crypto import RSA
from thc.crypto import Paillier
from thc.interfaces import Computation
from thc.utils import prime
from thc import THC
import random

class Product (Computation):
    def local (self, mod, args):
        a = args[0] % mod
        b = args[1] % mod
        return (a * b) % mod
    def remote (self, mod, args):
        return (args[0] * args[1]) % mod

class CorruptedProduct (Product):
    def remote (self, mod, args):             # overriding the "remote computation"
        f = random.randint(1, mod)            # with a random fault injection
        return (f + args[0] * args[1]) % mod

rsa = RSA(prime(1024), prime(1024), 65537)

thc = THC(rsa, Product(), 3)
print("43 × 47 =", thc.compute([43, 47])) # 2021

thc = THC(rsa, CorruptedProduct(), 3)
print("43 × 47 =", thc.compute([43, 47])) # False

pai = Paillier(prime(1024), prime(1024))

thc = THC(pai, Product(), 3)
print("43 + 47 =", thc.compute([43, 47])) # 90

thc = THC(pai, CorruptedProduct(), 3)
print("43 + 47 =", thc.compute([43, 47])) # False
