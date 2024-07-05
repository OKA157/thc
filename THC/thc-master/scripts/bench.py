from math import sqrt
import sqlite3

def means (stat):
    mean_N = sum([t['N'] for t in stat]) / len(stat)
    mean_Nr = sum([t['Nr'] for t in stat]) / len(stat)
    mean_r = sum([t['r'] for t in stat]) / len(stat)
    return {
        'N':  mean_N,
        'Nr': mean_Nr,
        'r':  mean_r
    }

def variances (stat):
    m = means(stat)
    var_N = sum([pow(t['N'] - m['N'], 2) for t in stat]) / len(stat)
    var_Nr = sum([pow(t['Nr'] - m['Nr'], 2) for t in stat]) / len(stat)
    var_r = sum([pow(t['r'] - m['r'], 2) for t in stat]) / len(stat)
    return {
        'N':  var_N,
        'Nr': var_Nr,
        'r':  var_r
    }

def deviations (stat):
    v = variances(stat)
    return {
        'N':  sqrt(v['N'])  * 1000,
        'Nr': sqrt(v['Nr']) * 1000,
        'r':  sqrt(v['r'])  * 1000
    }

def do_stats (data):
    stats = {}
    for row in data:
        if row['algo'] not in stats:
            stats[row['algo']] = {}
        if row['size'] not in stats[row['algo']]:
            stats[row['algo']][row['size']] = []
        stats[row['algo']][row['size']].append({
            'N': row['N'],
            'Nr': row['Nr'],
            'r': row['r']
        })
    return stats

def do_devs (stats):
    dev = {}
    for algo in stats:
        dev[algo] = {}
        for size in stats[algo]:
            dev[algo][size] = deviations(stats[algo][size])
    return dev

def do_print (dev, sum_data):
    print('ALGO\tSIZE\t#RUN\tTIME N\t\tTIME Nr\t\tTIME r\t\tCOST')
    for row in sum_data:
        N =  ((row['N'] / row['nb'])  * 1000)
        Nr = ((row['Nr'] / row['nb']) * 1000)
        r =  ((row['r'] / row['nb'])   * 1000)
        cost =  Nr - N + r
        cost_pc = (cost / N) * 100
        print("%s\t%d\t%d\t%03.3f\\pm{%03.2f} & %03.3f\\pm{%03.2f} & %03.3f\\pm{%03.2f} & %.2f\\%% \\\\" %
              (row['algo'].replace('elgamal', 'elg').replace('paillier', 'pai'),
               row['size'],
               row['nb'],
               N, dev[row['algo']][row['size']]['N'],
               Nr, dev[row['algo']][row['size']]['Nr'],
               r, dev[row['algo']][row['size']]['r'],
               cost_pc))

def do_analyses (db_file):
    db = sqlite3.connect(db_file)
    db.row_factory = sqlite3.Row
    sum_data = db.execute('select algo, size, sum(time_N) as N, sum(time_Nr) as pqr, sum(time_r) as r, count(*) as nb from bench group by algo, size').fetchall();
    data = db.execute('select algo, size, time_N as N, time_Nr as Nr, time_r as r from bench').fetchall();
    do_print(do_devs(do_stats(data)), sum_data)
    db.close()

do_analyses('data-bench.db')
do_analyses('data-bench-rsa.db')
