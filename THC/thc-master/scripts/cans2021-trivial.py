from thc.interfaces import HomomorphicCryptosystem, Computation
from thc import THC
import readline

class Field (HomomorphicCryptosystem):
    def __init__ (self, p):
        self._p = p
    def get_modulus (self):
        return self._p
    def encrypt (self, m):
        return m % self._p
    def decrypt (self, c):
        return c % self._p
    def mod (self, c, mod):
        return c % mod


class Linear (Computation):
    def __init__ (self, a, b):
        self.a = a
        self.b = b

    def local (self, mod, args):
        a = self.a % mod
        b = self.b % mod
        x = args[0] % mod
        print(f"\nlocal> computing {a}x + {b} = ? [{mod}]")
        print(f"local> with x = {x}")
        res = (a * x + b) % mod
        print(f"local> result: {res}\n")
        return res

    def remote (self, mod, args):
        print(f"remote> requested computation: {self.a}x + {self.b} = ? [{mod}]")
        print(f"remote> with x = {args[0]}")
        res = (self.a * args[0] + self.b) % mod
        print(f"remote> actual result: {res}\n")
        readline.set_startup_hook(lambda: readline.insert_text(f"{res}"))
        return int(input("remote> return? "))


thc = THC(Field(p=59233), Linear(42, 51), 17)
print(thc.compute([2021]))
