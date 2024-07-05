from random import seed, randint, choice
from functools import reduce
from thc.crypto.paillier import Paillier
from thc.utils import prime
from thc import THC

seed(1)

USE_THC = input('Should we use THC? (y/N): ') == 'y'

total = 50
campaign_at = 20

paillier = Paillier(prime(768), prime(768))

if not USE_THC:
    mod = paillier.get_modulus()
else:
    r = prime(32)
    mod = paillier.get_modulus() * r
    thc = THC(paillier, None, r)

ballots = []
if USE_THC:
    ballots_r = []

def cast_vote (choice):
    print(f'New vote: {choice}')
    if choice == 'yes':
        y, n = paillier.encrypt(1), paillier.encrypt(0)
    elif choice == 'no':
        y, n = paillier.encrypt(0), paillier.encrypt(1)
    else:
        y, n = paillier.encrypt(0), paillier.encrypt(0)
    ballots.append((y, n))
    if USE_THC:
        ballots_r.append((y % r, n % r))

check = { 'yes': 0, 'no': 0 }
for i in range(campaign_at):
    c = choice(['yes', 'no'])
    check[c] += 1
    cast_vote(c)
# print('[debug]', check)
print('> Here a campaign for the "yes" happens.')
for i in range(total - campaign_at):
    c = choice(['yes', 'yes', 'yes', 'no'])
    check[c] += 1
    cast_vote(c)
# print('[debug]', check)
    
def result (votes, m):
    return reduce(lambda a, b: (a * b) % m, votes)

CHEAT = input('Is there an attempt to manipulate the vote? (y/N): ') == 'y'

if CHEAT:
    forged_ballots = []
    for i in range(len(ballots)):
        forged_ballots.append(ballots[randint(0, campaign_at)])

if not CHEAT:
    res_y = result([b[0] for b in ballots], mod)
    res_n = result([b[1] for b in ballots], mod)
else:
    res_y = result([b[0] for b in forged_ballots], mod)
    res_n = result([b[1] for b in forged_ballots], mod)

if not USE_THC:
    yes, no = paillier.decrypt(res_y), paillier.decrypt(res_n)
else:
    res_y_r = result([b[0] for b in ballots_r], r)
    res_n_r = result([b[1] for b in ballots_r], r)
    yes, no = thc.verify(res_y, res_y_r), thc.verify(res_n, res_n_r)

print(f'Yes: {yes}\nNo:  {no}')
