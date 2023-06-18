def knapSack(weight_capacity, weights, values, items_count):
    # Initialize a matrix to store the maximum value for each remaining capacity and item count
    dp_matrix = [[0 for _ in range(weight_capacity + 1)] for _ in range(items_count + 1)]

    # Fill the matrix using a bottom-up approach
    for i in range(1, items_count + 1):
        for w in range(1, weight_capacity + 1):
            # If the current item's weight is less than or equal to the remaining capacity
            if weights[i-1] <= w:
                # Include the item and update the maximum value
                dp_matrix[i][w] = max(values[i-1] + dp_matrix[i-1][w-weights[i-1]], dp_matrix[i-1][w])
            else:
                # Do not include the item and carry forward the maximum value from the previous row
                dp_matrix[i][w] = dp_matrix[i-1][w]

    # The value at the last row and column represents the maximum value for the given weight capacity
    return dp_matrix[items_count][weight_capacity]

# Example usage:
values = [60, 100, 120]  # The values of the items
weights = [10, 20, 30]  # The weights of the items
weight_capacity = 50  # The maximum weight the knapsack can carry
items_count = len(values)  # The number of items available

maximum_value = knapSack(weight_capacity, weights, values, items_count)
print("Maximum value the knapsack can hold:", maximum_value)