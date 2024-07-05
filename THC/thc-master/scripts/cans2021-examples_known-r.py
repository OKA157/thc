from thc.crypto import RSA
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
    def __init__ (self, r):
        self._r = r
    def remote (self, mod, args):              # corrupt the "remote computation"
        f = random.randint(1, mod) * self._r   # with a multiple of r
        return (f + args[0] * args[1]) % mod

rsa = RSA(prime(1024), prime(1024), 65537)

thc = THC(rsa, Product(), prime(32))
print("[clean]     43 × 47 =", thc.compute([43, 47])) # 2021

r = prime(32)
thc = THC(rsa, CorruptedProduct(r), r)
print("\n[corrupted] 43 × 47 =", thc.compute([43, 47])) # ?
