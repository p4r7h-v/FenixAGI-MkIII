import scipy.stats as stats

def analyze_ab_test_results(visitors_a, conversions_a, visitors_b, conversions_b):
    # Calculate conversion rates for both variations
    conversion_rate_a = conversions_a / visitors_a
    conversion_rate_b = conversions_b / visitors_b

    # Perform Chi-square test for independence
    contingency_table = [[conversions_a, visitors_a - conversions_a],
                         [conversions_b, visitors_b - conversions_b]]
    chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)

    # Calculate the lift (improvement)
    lift = (conversion_rate_b - conversion_rate_a) / conversion_rate_a

    return {
        "conversion_rate_a": conversion_rate_a,
        "conversion_rate_b": conversion_rate_b,
        "chi2": chi2,
        "p_value": p_value,
        "lift": lift
    }

# Example usage of the function
visitors_a = 1000
conversions_a = 50
visitors_b = 1000
conversions_b = 70

result = analyze_ab_test_results(visitors_a, conversions_a, visitors_b, conversions_b)
print(result)