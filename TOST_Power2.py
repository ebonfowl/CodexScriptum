from scipy import optimize
import numpy as np
from scipy import stats


def tost_power(n, alpha, delta, cv):
    """Calculate the power of a TOST."""
    mt1 = -(delta * np.sqrt(n)) / cv
    mt2 = (delta * np.sqrt(n)) / cv
    ta = stats.t.ppf(1 - alpha, df=n - 1)
    power = stats.t.cdf(mt2 - ta, df=n-1) - stats.t.cdf(mt1 + ta, df=n-1)
    # Change negative values for power to 0
    try:
        power[power < 0] = 0
    except TypeError:
        pass

    return power


def func(n):
    """Generate a residual to minimise."""
    res = tost_power(n, alpha, delta, cv) - desired_power

    return res

# Significance level/sensitivity of the test
alpha = 0.05
# Acceptance region/bound/magnitude of region of similarity
delta = 0.1  # 10%
# Coefficient of variation
cv = 0.25


# Desired power
desired_power = 0.8
# Give a range of sample sizes in which the optimiser can search
min_guess = 2
max_guess = 100
# Find the number of participants that gives the desired power level
sol = optimize.brentq(func, min_guess, max_guess)
print(sol)