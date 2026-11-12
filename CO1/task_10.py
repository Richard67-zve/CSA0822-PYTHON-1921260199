
from decimal import Decimal
from time import perf_counter


def total_float(payments):
    return sum(float(p) for p in payments)


def total_decimal(payments):
    return sum((Decimal(p) for p in payments), Decimal("0.00"))


def rate_per_litre(fat, snf):
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    return round(30 + fat_steps * 0.40 + snf_steps * 0.30, 2)


# Compare totals and execution times
for n in [300, 6000, 150000]:
    payments = (["33.40", "0.10", "27.80"] * ((n + 2) // 3))[:n]

    start = perf_counter()
    f_total = total_float(payments)
    float_time = perf_counter() - start

    start = perf_counter()
    d_total = total_decimal(payments)
    decimal_time = perf_counter() - start

    rounded_float = round(f_total, 2)

    print(f"\nPayments: {n}")
    print(f"Float total:   {rounded_float:.2f}")
    print(f"Decimal total: {d_total:.2f}")
    print(f"Difference:    {abs(Decimal(str(rounded_float)) - d_total):.2f}")
    print(f"Float time:    {float_time:.6f} seconds")
    print(f"Decimal time:  {decimal_time:.6f} seconds")

    # Compare rounding each payment vs rounding the final total
    each_rounded = round(sum(round(float(p), 2) for p in payments), 2)
    print(f"Round each:    {each_rounded:.2f}")


# Compare rate recalculation with dictionary caching
entries = [(4.2, 8.7), (3.5, 8.5), (3.1, 8.3)] * 10000

start = perf_counter()
rates_direct = [rate_per_litre(fat, snf) for fat, snf in entries]
direct_time = perf_counter() - start

start = perf_counter()
rate_cache = {}
rates_cached = []

for fat, snf in entries:
    key = (fat, snf)
    if key not in rate_cache:
        rate_cache[key] = rate_per_litre(fat, snf)
    rates_cached.append(rate_cache[key])

cached_time = perf_counter() - start

print("\nRATE CACHING")
print(f"Direct calculation: {direct_time:.6f} seconds")
print(f"Cached lookup:      {cached_time:.6f} seconds")
print(f"Different rate pairs: {len(rate_cache)}")
