import sys
import random
import time
from thc import THC
from thc.utils import prime
from thc.crypto.elgamal import ElGamal
from thc.demo._computations import PairProduct
import sqlite3

if __name__ ==  '__main__':

    r_sizes = [2, 4, 8, 16, 32]
    nb_series = 10
    nb_tests_per_serie = 100
    nb_repeat_per_test = 1000

    db = sqlite3.connect('data-bench.db')
    algo = 'elgamal-prod-2048'
    comp = PairProduct()

    for size in r_sizes:
        print('> Size is ' + str(size))
        for s in range(nb_series):
            print('> Tests serie #' + str(size) + '.' + str(s))
            print('> Generating a fresh ElGamal instance… ', end='')
            elg = ElGamal.new(2048)
            print('done.')

            r = prime(size)
            print('> r is ' + str(r))

            N = elg.get_modulus()
            Nr = N * r

            thc = THC(elg, comp, r)

            data = []
            for t in range(nb_tests_per_serie):
                print('> Test #' + str(size) + '.' + str(s) + '.' + str(t) + ':')

                nums = [random.randint(0, elg.get_modulus())
                        for _ in range(0, 5)]
                nums_enc_N = [elg.encrypt(n) for n in nums]

                start_N = time.process_time()
                for _ in range(nb_repeat_per_test):
                    res_N = comp.local(N, nums_enc_N)
                time_N = time.process_time() - start_N

                print('Time in Z_N:  ' + str(time_N) + ' s')

                nums_enc_Nr = [elg.mod(n, Nr) for n in nums_enc_N]

                start_Nr = time.process_time()
                for _ in range(nb_repeat_per_test):
                    res_Nr = comp.local(Nr, nums_enc_Nr)
                time_Nr = time.process_time() - start_Nr

                print('Time in Z_Nr: ' + str(time_Nr) + ' s')

                nums_enc_r = [elg.mod(n, r) for n in nums_enc_Nr]

                start_r = time.process_time()
                for _ in range(nb_repeat_per_test):
                    res_r = comp.local(r, nums_enc_r)
                time_r = time.process_time() - start_r

                print('Time in F_r:  ' + str(time_r) + ' s')

                # start_verif = time.process_time()
                # for _ in range(nb_repeat_per_test):
                res = thc.verify(res_Nr, res_r)
                # time_verif = time.process_time() - start_verif

                # print('Verif time:    ' + str(time_verif) + ' s')
                time_verif = 0

                if res is not False:
                    print('Success.')
                else:
                    print('Failure.')

                data.append((algo, size, time_N, time_Nr, time_r, time_verif))
            db.executemany('INSERT INTO bench VALUES (?, ?, ?, ?, ?, ?)',
                           data)
            db.commit()

    db.close()
