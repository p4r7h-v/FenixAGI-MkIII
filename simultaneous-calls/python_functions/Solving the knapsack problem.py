def knapSack(weight_capacity, weights, values, item_count):
    # Create a table to store the max value for each weight capacity and item index
    K = [[0 for w in range(weight_capacity + 1)] for i in range(item_count + 1)]

    # Loop through the items and weight capacities to fill the table
    for i in range(item_count + 1):
        for w in range(weight_capacity + 1):
            # Base case - no items or weight capacity left
            if i == 0 or w == 0:
                K[i][w] = 0
            # If the current item's weight is less than or equal to the remaining capacity
            elif weights[i-1] <= w:
                # Determine the higher value between including or excluding the current item
                K[i][w] = max(values[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
            else:
                # If the item cannot be included, simply use the value from the previous item
                K[i][w] = K[i-1][w]

    # The final result will be stored in the bottom-right cell of the table
    return K[item_count][weight_capacity]

# Example usage:
values = [60, 100, 120]
weights = [10, 20, 30]
weight_capacity = 50
item_count = len(values)
print(knapSack(weight_capacity, weights, values, item_count))  # Output: 220