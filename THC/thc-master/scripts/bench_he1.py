import sys
import random
import time
from thc import THC
from thc.utils import prime
from thc.crypto.he1 import HE1
from thc.demo._computations import RandomBinaryPolynomial
import sqlite3

if __name__ ==  '__main__':

    r_sizes = [2, 4, 8, 16, 32]
    nb_series = 10
    nb_tests_per_serie = 10
    nb_comp_per_test = 10
    nb_repeat_per_comp = 1000

    db = sqlite3.connect('data-bench.db')
    algo = 'he1-poly-2048'

    for size in r_sizes:
        print('> Size is ' + str(size))
        for s in range(nb_series):
            print('> Tests serie #' + str(size) + '.' + str(s))
            print('> Generating a fresh HE1 instance… ', end='')
            he1 = HE1.new(256)
            print('done.')

            r = prime(size)
            print('> r is ' + str(r))

            N = he1.get_modulus()
            Nr = N * r

            for t in range(nb_tests_per_serie):
                print('> Test #' + str(size) + '.' + str(s) + '.' + str(t) + ': ', end='')
                comp = RandomBinaryPolynomial(5, N)
                comp_r = comp.mod(r)
                print('P(x, y) = ' + str(comp))

                thc = THC(he1, comp, r)

                data = []
                for c in range(nb_comp_per_test):
                    print('> Computation #' + str(size) + '.' +
                          str(s) + '.' + str(t) + '.' + str(c) + ':')
                    x = random.randint(0, N - 1)
                    y = random.randint(0, N - 1)

                    x_enc = he1.encrypt(x) % N
                    y_enc = he1.encrypt(y) % N
                    xy_enc = [x_enc, y_enc]

                    start_N = time.process_time()
                    for _ in range(nb_repeat_per_comp):
                        res_N = comp.local(N, xy_enc)
                    time_N = time.process_time() - start_N

                    print('Time in Z_N:  ' + str(time_N) + ' s')

                    xNr_enc = x_enc % Nr
                    yNr_enc = y_enc % Nr
                    xyNr_enc = [xNr_enc, yNr_enc]

                    start_Nr = time.process_time()
                    for _ in range(nb_repeat_per_comp):
                        res_Nr = comp.local(Nr, xyNr_enc)
                    time_Nr = time.process_time() - start_Nr

                    print('Time in Z_Nr: ' + str(time_Nr) + ' s')

                    xr_enc = x_enc % r
                    yr_enc = y_enc % r
                    xyr_enc = [xr_enc, yr_enc]

                    start_r = time.process_time()
                    for _ in range(nb_repeat_per_comp):
                        res_r = comp_r.local(r, xyr_enc)
                    time_r = time.process_time() - start_r

                    print('Time in F_r:  ' + str(time_r) + ' s')

                    # start_verif = time.process_time()
                    # for _ in range(nb_repeat_per_comp):
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
