import sqlite3

db = sqlite3.connect('data-pnd.db')
db.row_factory = sqlite3.Row

data = db.execute('select algo, size, sum(missed) as missed, sum(total) as total from pnd group by algo, size').fetchall();

print('ALGO\t\tSIZE\tTOTAL\tMISSED\tPND')
for r in data:
    pnd = r['missed'] / r['total']
    print(r['algo'] + '\t' +
          str(r['size']) + '\t' +
          str(r['total']) + '\t' +
          str(r['missed']) + '\t' +
          str(pnd))

db.close()
