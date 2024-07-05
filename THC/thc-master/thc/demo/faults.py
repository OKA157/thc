import argparse
import random
from .. import THC
from ..utils import prime
from ..crypto.trivial import Trivial
from ..crypto.rsa import RSA
from ..crypto.elgamal import ElGamal
from ..crypto.paillier import Paillier
from ..crypto.he1 import HE1
from ._computations import Product, PairProduct, RandomPolynomial

if __name__ ==  '__main__':

    ap = argparse.ArgumentParser(description='THC random faults demo.')
    ap.add_argument('-m', '--mod_size', type=int, default=512,
                    help='modulus size for cryptosystems')
    ap.add_argument('-r', '--r_size', type=int, default=32,
                    help='modular extension parameter size')
    args = ap.parse_args()

    nums = random.sample(range(2**8), 5)

    ### RSA

    thc = THC(RSA.new(args.mod_size), Product(), prime(args.r_size))
    print('> Multiplications with RSA:')
    print(' * '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### ElGamal

    thc = THC(ElGamal.new(args.mod_size), PairProduct(), prime(args.r_size))
    print('> Multiplications with ElGamal:')
    print(' * '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### Paillier

    thc = THC(Paillier.new(args.mod_size), Product(), prime(args.r_size))
    print('> Additions with Paillier:')
    print(' + '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### HE1

    rp = RandomPolynomial(5, 2**8)
    thc = THC(HE1.new(args.mod_size // 2), rp, prime(args.r_size))
    print('> Polynomial with HE1:')
    print('random polynomial P(x) =', rp)
    for n in nums:
        print('P(' + str(n) + ') =', thc.compute([n]))
