import datetime

def calculate_churn_rate(customers):
    """
    Calculate the churn rate of customers.

    Args:
      customers (list): List of dictionaries containing customer data with keys 'signup_date', 'last_active_date', and 'is_churned'.

    Returns:
    float: Churn rate as a percentage.
    """

    if not customers:
        return 0.0

    churned_customers = 0
    active_customers = 0

    for customer in customers:
        if customer['is_churned']:
            churned_customers += 1
        if customer['last_active_date'] > customer['signup_date']:
            active_customers += 1

    if active_customers == 0:
        return 0.0

    churn_rate = (churned_customers / active_customers) * 100

    return churn_rate

# Example usage:
customers_data = [
    {'signup_date': datetime.date(2021, 1, 1), 'last_active_date': datetime.date(2021, 2, 1), 'is_churned': False},
    {'signup_date': datetime.date(2021, 1, 2), 'last_active_date': datetime.date(2021, 2, 2), 'is_churned': True},
    {'signup_date': datetime.date(2021, 1, 3), 'last_active_date': datetime.date(2021, 2, 3), 'is_churned': False},
    {'signup_date': datetime.date(2021, 1, 4), 'last_active_date': datetime.date(2021, 1, 25), 'is_churned': True},
]

churn_rate = calculate_churn_rate(customers_data)

print("The churn rate is: {:.2f}%".format(churn_rate))