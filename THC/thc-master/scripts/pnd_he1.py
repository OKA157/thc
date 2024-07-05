import sys
import random
from thc import THC
from thc.utils import prime
from thc.crypto.he1 import HE1
from thc.demo._computations import Product, RandomBinaryPolynomial

if __name__ ==  '__main__':

    r_sizes = [2, 4, 8, 16, 32]
    r_sizes = [32]
    nb_series = 1000
    nb_tests_per_serie = {
        2: 90,
        4: 50,
        8: 1000,
        16: 5000,
        32: 10000
    }

    # f = open('pnd_he1-poly.txt', 'w')
    f = open('pnd_he1-prod_32.txt', 'w')
    comp = Product()

    for size in r_sizes:
        print('> Size is ' + str(size))
        for s in range(nb_series):
            noerr = missed = detected = 0
            print('> Tests serie #' + str(size) + '.' + str(s))
            print('> Generating a fresh HE1 instance… ', end='')
            sys.stdout.flush()
            he1 = HE1(prime(1024), prime(2048))
            print('done.')
            r = prime(size)
            print('> r is ' + str(r))
            # comp = RandomBinaryPolynomial(5, he1.get_modulus())
            thc = THC(he1, comp, r)
            for t in range(nb_tests_per_serie[size]):
                print('> Test #' + str(size) + '.' + str(s) + '.' + str(t) + ': ', end='')
                # xy = [random.randint(0, he1.get_modulus()), random.randint(0, he1.get_modulus())]
                # result = thc.compute(xy)
                # valid = comp.local(he1.get_modulus(), xy) % he1.get_modulus()
                nums = [random.randint(0, he1.get_modulus())
                        for _ in range(0, 5)]
                result = thc.compute(nums)
                valid = comp.local(he1.get_modulus(), nums) % he1.get_modulus()
                if valid == result:
                    print('> no error')
                    noerr += 1
                elif result is False:
                    print('> error detected')
                    detected += 1
                else:
                    print('> error missed')
                    missed += 1
                print()
            f.write('size ' + str(size) + '\t' +
                    'r ' + str(r) + '\t' +
                    'noerr ' + str(noerr) + '\t' +
                    'missed ' + str(missed) + '\t' +
                    'detected ' + str(detected) + '\t' +
                    'total ' + str(nb_tests_per_serie[size]) + '\n')
    f.close()
