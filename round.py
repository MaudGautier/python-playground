""" Rounding always rounds to the even number when x.5
Called the bankers rounding
-> https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers
Solved with ROUND_HALF_UP from decimal
"""

print("# Standard rounding")
for i in range(1, 15, 2):
    n = i / 2
    print(n, "=>", round(n))

# Prints:
# 0.5 => 0
#  1.5 => 2
#  2.5 => 2
#  3.5 => 4
#  4.5 => 4
#  5.5 => 6
#  6.5 => 6

# With decimal:
from decimal import localcontext, Decimal, ROUND_HALF_UP
print("\n# Rounding with decimal (ROUND_HALF_UP)")
with localcontext() as ctx:
    ctx.rounding = ROUND_HALF_UP
    for i in range(1, 15, 2):
        n = Decimal(i) / 2
        print(n, '=>', n.to_integral_value())

# Prints:
#  0.5 => 1
#  1.5 => 2
#  2.5 => 3
#  3.5 => 4
#  4.5 => 5
#  5.5 => 6
#  6.5 => 7
