import numpy as np
import scipy.stats as stats

def ab_test(n_a, n_b, click_a, click_b):
    # Calculate click through rate (CTR)
    ctr_a = click_a/n_a
    ctr_b = click_b/n_b

    # Function stats.binom.interval calculates Confidence Interval (CI) for binominal distribution 
    ci_a = stats.binom.interval(0.95, n_a, ctr_a)
    ci_b = stats.binom.interval(0.95, n_b, ctr_b)

    # Normalize CI by size of groups and calculate difference
    diff = (ci_b[0]/n_b - ci_a[1]/n_a)

    if diff > 0:
        print('Version B of the webpage performs significantly better with a confidence of 0.95. You should switch to version B!')
    else:
        print('We cannot say that version B of the webpage performs better with a confidence of 0.95. Stick to version A for now!')

# Running the A/B testing on two versions
ab_test(1000, 1200, 300, 370)