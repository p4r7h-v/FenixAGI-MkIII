def prime_factors(n):
    factors = []
    # Remove any factors of 2
    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    # Check for odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i

    # If n is a prime number greater than 2, add it to the list
    if n > 2:
        factors.append(n)

    return factors