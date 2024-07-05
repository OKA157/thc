import sys
import random
from thc import THC
from thc.utils import prime
from thc.crypto.rsa import RSA
from thc.demo._computations import Product

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

    f = open('pnd_rsa-prod_32.txt', 'w')

    comp = Product()

    for size in r_sizes:
        print('> Size is ' + str(size))
        for s in range(nb_series):
            noerr = missed = detected = 0
            print('> Tests serie #' + str(size) + '.' + str(s))
            print('> Generating a fresh RSA instance… ', end='')
            sys.stdout.flush()
            rsa = RSA.new()
            print('done.')
            r = prime(size)
            print('> r is ' + str(r))
            thc = THC(rsa, comp, r)
            for t in range(nb_tests_per_serie[size]):
                print('> Test #' + str(size) + '.' + str(s) + '.' + str(t) + ': ', end='')
                nums = [random.randint(0, rsa.get_modulus())
                        for _ in range(0, 5)]
                # print('Nums are: ' + str(nums))
                result = thc.compute(nums)
                valid = comp.local(rsa.get_modulus(), nums) % rsa.get_modulus()
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
