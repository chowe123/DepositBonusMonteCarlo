import random

# Example slot payout distribution (approx 97% RTP BEFORE normalization)
raw_dist = [
    (0.83, 0.0),
    (0.07, 1.0),
    (0.04, 2.0),
    (0.025, 4.0),
    (0.015, 8.0),
    (0.01, 15.0),
    (0.007, 30.0),
    (0.002, 45.0),
    (0.001, 150.0)
]

# --- Normalize probabilities to ensure sum = 1 ---
total_p = sum(p for p, _ in raw_dist)
dist = [(p / total_p, payout) for p, payout in raw_dist]

# --- Verify probability sum ---
assert abs(sum(p for p, _ in dist) - 1.0) < 1e-9

# --- Calculate RTP ---
def calc_rtp(dist):
    return sum(p * payout for p, payout in dist)

print(f"Theoretical RTP: {calc_rtp(dist):.4f}")

# --- Spin function (robust) ---
def spin(dist):
    r = random.random()
    cumulative = 0
    for p, payout in dist:
        cumulative += p
        if r < cumulative:
            return payout
    return dist[-1][1]  # fallback safety

# --- Single bonus run ---
def run_bonus(bet_size, balance, wager_required):
    wagered = 0
    while wagered < wager_required:
        if balance < bet_size:
            return 0, False, wagered  # busted

        payout = spin(dist)
        result = payout * bet_size

        balance += result - bet_size
        wagered += bet_size

    return balance, True, wagered  # completed wagering

# --- Simulation ---
def simulate(bet_size, trials=50, balance=200, wager_required=6000):
    total_return = 0
    completions = 0
    total_wagered = 0

    for _ in range(trials):
        final_balance, completed, wagered = run_bonus(bet_size, balance=balance, wager_required=wager_required)
        total_return += final_balance
        total_wagered += wagered

        if completed:
            completions += 1

    avg_return = total_return / trials
    completion_rate = completions / trials
    avg_wagered = total_wagered / trials

    return avg_return, completion_rate, avg_wagered



balance=200
wager_required=6000
print(f"Running Monte Carlo | Starting Balance = {balance} | Wager Requirement = {wager_required}")
# --- Run tests ---
for bet in [1, 2, 5, 10, 20, 40]:

    ev, comp, avg_wag = simulate(bet, trials=10000)
    print(f"Bet: ${bet}")
    print(f"  Avg Return: ${ev:.2f}")
    print(f"  Completion Rate: {comp:.2%}")
    print(f"  Avg Wagered: ${avg_wag:.2f}")
    print()